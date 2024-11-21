FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

COPY mnist.py /app/mnist.py

RUN pip install --no-cache-dir argparse numpy

RUN apt-get update && apt-get install -y ca-certificates \
    && pip install --no-cache-dir argparse numpy \
    && update-ca-certificates

CMD ["python3", "/app/mnist.py"]
