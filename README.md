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


# Set up Hugging Face to use Llama-3.2-1B llm 

## 1. Go to https://huggingface.co/meta-llama/Llama-3.2-1B and request access to the model
![image](https://github.com/user-attachments/assets/0a475a69-bb2b-4835-947f-b43f4d22c8f8)
## 2. Create an access token (if doesn't have one already)
Log into HG, click on the profile picture of the account, select 'Access Tokens'.

![image](https://github.com/user-attachments/assets/87512a5b-05e1-41a6-987c-98a6394209a0)

Click on 'Create new token' if you don't have an active token.
![image](https://github.com/user-attachments/assets/eb369332-513a-4e8d-a7b4-b19cf01d7b48)
Select 'Read' for Token type, input a name for the token.
![image](https://github.com/user-attachments/assets/94da2371-16fa-401e-810d-413bab3604d3)
Once the token is generated, copy it and save it to a txt file locally for future use.
## 3. Log into Huggingface CLI
Open a new terminal/command line instance.
In the working environment selected, run:

    huggingface-cli login

You should see the following output in the command line (or something similar):
![image](https://github.com/user-attachments/assets/047e5bb3-3ba4-4d3e-bada-584f32f35fcd)
Open the local txt file that has the HF access token saved, copy and paste the access token to the command line.
Adding token to the git-credential is optional.
The end result should look something like this to confirm successful login:

![image](https://github.com/user-attachments/assets/1097c1d5-5d12-4aff-b213-ff6eda45a815)

## 4. Once the login is successful, run the backend.





