
import os
import json

import tensorflow as tf
import mnist # Your module

# Define batch size
per_worker_batch_size = 64

# Get TF_CONFIG from the env variables and save it as JSON
tf_config = json.loads(os.environ['TF_CONFIG'])

# Infer number of workers from tf_config
num_workers = len(tf_config['cluster']['worker'])

# Define strategy
strategy = tf.distribute.MultiWorkerMirroredStrategy()

# Define global batch size
global_batch_size = per_worker_batch_size * num_workers

# Load dataset
multi_worker_dataset = mnist.mnist_dataset(global_batch_size)

# Create and compile model following the distributed strategy
with strategy.scope():
  multi_worker_model = mnist.build_and_compile_cnn_model()

# Train the model
multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)
