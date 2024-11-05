
import tensorflow as tf
import tensorflow_transform as tft

import traffic_constants

# Unpack the contents of the constants module
_DENSE_FLOAT_FEATURE_KEYS = traffic_constants.DENSE_FLOAT_FEATURE_KEYS
_RANGE_FEATURE_KEYS = traffic_constants.RANGE_FEATURE_KEYS
_VOCAB_FEATURE_KEYS = traffic_constants.VOCAB_FEATURE_KEYS
_VOCAB_SIZE = traffic_constants.VOCAB_SIZE
_OOV_SIZE = traffic_constants.OOV_SIZE
_CATEGORICAL_FEATURE_KEYS = traffic_constants.CATEGORICAL_FEATURE_KEYS
_BUCKET_FEATURE_KEYS = traffic_constants.BUCKET_FEATURE_KEYS
_FEATURE_BUCKET_COUNT = traffic_constants.FEATURE_BUCKET_COUNT
_VOLUME_KEY = traffic_constants.VOLUME_KEY
_transformed_name = traffic_constants.transformed_name


def preprocessing_fn(inputs):
    """tf.transform's callback function for preprocessing inputs.
    Args:
    inputs: map from feature keys to raw not-yet-transformed features.
    Returns:
    Map from string feature key to transformed feature operations.
    """
    outputs = {}

    ### START CODE HERE
    
    # Scale these features to the z-score.
    for key in _DENSE_FLOAT_FEATURE_KEYS:
        # Scale these features to the z-score.
        outputs[_transformed_name(key)] = tft.scale_to_z_score(inputs[key])
            

    # Scale these feature/s from 0 to 1
    for key in _RANGE_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.scale_to_0_1(inputs[key])
            

    # Transform the strings into indices 
    # hint: use the VOCAB_SIZE and OOV_SIZE to define the top_k and num_oov parameters
    for key in _VOCAB_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.compute_and_apply_vocabulary(inputs[key],
                                                                           num_oov_buckets = _OOV_SIZE,
                                                                          top_k = _VOCAB_SIZE)
            
            
    # Bucketize the feature
    for key in _BUCKET_FEATURE_KEYS:
        outputs[_transformed_name(key)] = tft.bucketize(inputs[key], _FEATURE_BUCKET_COUNT[key])
            

    # Keep the features as is. No tft function needed.
    for key in _CATEGORICAL_FEATURE_KEYS:
        outputs[_transformed_name(key)] = inputs[key]

        
    # Use `tf.cast` to cast the label key to float32
    traffic_volume = tf.cast(inputs[_VOLUME_KEY], tf.float32)
  
    
    # Create a feature that shows if the traffic volume is greater than the mean and cast to an int
    outputs[_transformed_name(_VOLUME_KEY)] = tf.cast(          
        # Use `tf.greater` to check if the traffic volume in a row is greater than the mean of the entire traffic volumn column
        # Hint: Use a `tft` function to compute the mean.
        tf.greater(traffic_volume, tft.mean(tf.cast(inputs[_VOLUME_KEY], tf.float32))),
        
        tf.int64)                                        
    ### END CODE HERE
    return outputs
