# Use the latest PyTorch image that already includes torch and torchvision
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set the working directory inside the container
WORKDIR /app

# Copy the mnist.py script into the container
COPY mnist.py /app/mnist.py

# Install additional dependencies (if necessary)
RUN pip install --no-cache-dir argparse numpy

# Update CA certificates and install additional dependencies
RUN apt-get update && apt-get install -y ca-certificates \
    && pip install --no-cache-dir argparse numpy \
    && update-ca-certificates

# Set the default command to run the mnist.py script
CMD ["python3", "/app/mnist.py"]
