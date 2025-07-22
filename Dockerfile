

# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copy your application code AND your frontend code
COPY ./app ./app
COPY ./seed_db.py .

# Add the app directory to the PYTHONPATH for correct imports
ENV PYTHONPATH "${PYTHONPATH}:/app"

# The command to start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]