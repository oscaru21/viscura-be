# Setup Instructions

Follow these steps to set up a virtual environment, install the required packages, and serve the FastAPI application.

## 1. Create a Virtual Environment

```bash
python3.9 -m venv venv
```

## 2. Activate the Virtual Environment

### On macOS and Linux:

```bash
source venv/bin/activate
```

### On Windows:

```bash
.\venv\Scripts\activate
```
inside the venv folder add a .gitignore file with an * to ignore all the environment files

## 3. Install Requirements

```bash
pip install -r requirements.txt
```

## 4. Serve the FastAPI Application

```bash
uvicorn app.main:app --reload
```

Replace `main:app` with the appropriate module and application instance if different.

## 5. Build the Docker-Compose Database

Ensure you have the following prerequisites:
- Docker daemon running
- No other instances of PostgreSQL running
- Docker Compose installed

### Steps:

1. Navigate to the `vector_database` folder:

    ```bash
    cd vector_database
    ```

2. Build and start the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. To stop the containers, use:

    ```bash
    docker-compose down
    ```

Make sure to check the logs for any errors during the build process.

## 6. Set up Redis

Given that Docker daemon is running, run the following command:

    ```bash
    docker run --name redis -p 6379:6379 -d redis
    ```

Verify that redis is running after the container starts (optional):

    ```bash
    docker ps
    ```


# Set up Hugging Face  

## 1. Create an access token (if doesn't have one already)
Log into HG, click on the profile picture of the account, select 'Access Tokens'.

![image](https://github.com/user-attachments/assets/87512a5b-05e1-41a6-987c-98a6394209a0)

Click on 'Create new token' if you don't have an active token.
![image](https://github.com/user-attachments/assets/eb369332-513a-4e8d-a7b4-b19cf01d7b48)
Select 'Read' for Token type, input a name for the token.
![image](https://github.com/user-attachments/assets/94da2371-16fa-401e-810d-413bab3604d3)
Once the token is generated, copy it and save it to a txt file locally for future use.

## 2. Create an env variable with the token
Create a file named .env at the root of the project add a variable named `HUGGINGFACE_API_TOKEN` and input your token:
`HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

# UNIT TEST
## Run Unit Tests

To run the unit tests, navigate to the `app/tests` folder and run the following commands:

```bash
export PYTHONPATH=.
python -m unittest discover
```




