FROM python:3.8-slim

WORKDIR /app
COPY . /app
RUN pip install flask

EXPOSE 8080
CMD ["python", "app.py"]