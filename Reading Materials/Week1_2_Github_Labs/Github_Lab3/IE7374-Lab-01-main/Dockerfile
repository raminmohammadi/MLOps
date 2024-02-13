FROM python:slim

RUN mkdir /lab1
WORKDIR /lab1

RUN pip install numpy scipy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="MLOPS IE-7374 <mlops7374@gmail.com>" \version="1.0"


CMD ["python", "src/lab1.py"]
