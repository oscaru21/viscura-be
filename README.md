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