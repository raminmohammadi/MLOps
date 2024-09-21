FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model/ ./model/
COPY src/ ./src/

#This line tells Docker that the container will listen on the port specified by the environment variable PORT
EXPOSE $PORT 

CMD ["sh", "-c", "python src/main.py  --server.port $PORT"]
# sh to allow for accesing environmental variabels like $port
# -c to run this within the container