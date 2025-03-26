FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port 8080 for Flask
EXPOSE 8080

# Use Gunicorn to run Flask (better for production)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
