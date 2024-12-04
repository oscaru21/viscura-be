import redis
from passlib.context import CryptContext
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.services.database_service import DatabaseService
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
import os

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self):
        try:
            self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            self.redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
            self.redis_client.ping() 
        except redis.ConnectionError as e:
            raise Exception("Failed to connect to Redis server. Ensure Redis is running.")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, roles: List[str], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token with an optional expiration.
        """
        to_encode = data.copy()
        to_encode["roles"] = roles
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[dict]:
        """
        Decode the JWT access token and return the payload.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def blacklist_token(self, token: str, exp: int):
        """
        Add the token to the Redis blacklist with an expiration time.
        """
        try:
            current_timestamp = int(datetime.now(timezone.utc).timestamp())
            ttl = exp - current_timestamp
            if ttl <= 0:
                raise ValueError("Token expiration time has already passed.")  # This error
            self.redis_client.setex(token, ttl, "blacklisted")
            print(f"Token blacklisted successfully for {ttl} seconds.")
        except redis.ConnectionError as e:
            raise Exception(f"Redis connection error: {str(e)}")

    def is_token_blacklisted(self, token: str) -> bool:
        """
        Check if a token is blacklisted.
        """
        return self.redis_client.get(token) is not None

    def register_user(self, user_data: UserRegisterRequest) -> UserResponse:
        """
        Register a new user with the given information.
        """
        with DatabaseService() as db:
            password_hash = self.hash_password(user_data.password)
            user_id = db.insert_record("users", {
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "password_hash": password_hash
            })

            role_names = tuple(user_data.roles) 
            query = f"SELECT * FROM roles WHERE name IN %s"
            db.cursor.execute(query, (role_names,))
            roles_data = db.cursor.fetchall()

            if not roles_data:
                raise ValueError("One or more roles provided are invalid")

            role_ids = [role["id"] for role in roles_data]

            for role_id in role_ids:
                db.insert_record("user_roles", {"user_id": user_id, "role_id": role_id}, return_id=False)

            return UserResponse(
                id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email,
                roles=user_data.roles
            )


    def authenticate_user(self, login_data: UserLoginRequest) -> Optional[TokenResponse]:
        """
        Authenticate the user by email and password and return a token if successful.
        """
        with DatabaseService() as db:
            user_data = db.read_records("users", {"email": login_data.email})
            if not user_data:
                return None
            user = user_data[0]

            if self.verify_password(login_data.password, user["password_hash"]):
                query = """
                    SELECT roles.name
                    FROM user_roles
                    JOIN roles ON user_roles.role_id = roles.id
                    WHERE user_roles.user_id = %s
                """
                db.cursor.execute(query, (user["id"],))
                roles_data = db.cursor.fetchall()
                roles = [role["name"] for role in roles_data]  
                access_token = self.create_access_token(data={"sub": user["email"]}, roles=roles)
                return TokenResponse(access_token=access_token, token_type="bearer")
            return None

    def logout_user(self, token: str):
        """
        Blacklist the given token to log out the user.
        """
        try:
            payload = self.decode_access_token(token)
            if not payload:
                raise ValueError("Invalid token")

            exp = payload.get("exp")
            if not exp:
                raise ValueError("Token expiration (`exp`) not found")

            self.blacklist_token(token, exp)
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to blacklist token: {str(e)}")