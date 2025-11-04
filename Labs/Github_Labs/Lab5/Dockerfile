FROM python:3.9-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/model /app/logs

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the entire src folder
COPY src/ /app/src/

# Copy all Python files
#COPY *.py .

# Move to src directory
WORKDIR /app/src

# Expose port for FastAPI
EXPOSE 8000

# Train the model first, then start the API
CMD ["sh", "-c", "python train.py && uvicorn main:app --host 0.0.0.0 --port 8000"]