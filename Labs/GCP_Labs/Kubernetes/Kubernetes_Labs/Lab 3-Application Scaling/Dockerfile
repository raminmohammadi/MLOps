FROM python:3.10

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r /code/requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8080"]