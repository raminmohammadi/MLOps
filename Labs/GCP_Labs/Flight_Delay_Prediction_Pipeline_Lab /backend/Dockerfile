FROM python:3.9

WORKDIR /backend

RUN apt-get update && \
    apt-get install -y --no-install-recommends libomp-dev
    
COPY . .

RUN pip install --no-cache-dir -r /backend/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8080"]
# CMD ["python", "main.py"]