# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for Render (optional but helpful)
EXPOSE 10000

# Start the FastAPI app using the PORT Render provides
CMD ["sh", "-c", "uvicorn bot:app --host 0.0.0.0 --port $PORT"]

