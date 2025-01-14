
# import os
import tensorflow as tf
import numpy as np

def mnist_dataset(batch_size):
  # Load the data
  (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
  # Normalize pixel values for x_train and cast to float32
  x_train = x_train / np.float32(255)
  # Cast y_train to int64
  y_train = y_train.astype(np.int64)
  # Define repeated and shuffled dataset
  train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(60000).repeat().batch(batch_size)
  return train_dataset


def build_and_compile_cnn_model():
  # Define simple CNN model using Keras Sequential
  model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(28, 28)),
      tf.keras.layers.Reshape(target_shape=(28, 28, 1)),
      tf.keras.layers.Conv2D(32, 3, activation='relu'),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10)
  ])

  # Compile model
  model.compile(
      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
      metrics=['accuracy'])

  return model
