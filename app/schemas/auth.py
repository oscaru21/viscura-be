from typing import List, Optional
from pydantic import BaseModel, EmailStr
# schemas for requests and responses
class UserRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    roles: List[str]

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    roles: List[str]  