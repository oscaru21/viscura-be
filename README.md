# Setup Instructions

Follow these steps to set up a virtual environment, install the required packages, and serve the FastAPI application.

## 1. Create a Virtual Environment

```bash
python3 -m venv venv
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