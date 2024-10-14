
import tensorflow as tf
import tensorflow_transform as tft

import cover_constants

_SCALE_MINMAX_FEATURE_KEYS = cover_constants.SCALE_MINMAX_FEATURE_KEYS
_SCALE_01_FEATURE_KEYS = cover_constants.SCALE_01_FEATURE_KEYS
_SCALE_Z_FEATURE_KEYS = cover_constants.SCALE_Z_FEATURE_KEYS
_VOCAB_FEATURE_KEYS = cover_constants.VOCAB_FEATURE_KEYS
_HASH_STRING_FEATURE_KEYS = cover_constants.HASH_STRING_FEATURE_KEYS
_LABEL_KEY = cover_constants.LABEL_KEY
_transformed_name = cover_constants.transformed_name

def preprocessing_fn(inputs):

    features_dict = {}

    ### START CODE HERE ###
    for feature in _SCALE_MINMAX_FEATURE_KEYS:
        data_col = inputs[feature]         
        # Transform using scaling of min_max function
        # Hint: Use tft.scale_by_min_max by passing in the respective column
        # Use the *default* output range of the function
        features_dict[_transformed_name(feature)] = tft.scale_by_min_max(data_col)

    for feature in _SCALE_01_FEATURE_KEYS:
        data_col = inputs[feature]         
        # Transform using scaling of 0 to 1 function
        # Hint: tft.scale_to_0_1
        features_dict[_transformed_name(feature)] = tft.scale_to_0_1(data_col)

    for feature in _SCALE_Z_FEATURE_KEYS:
        data_col = inputs[feature]         
        # Transform using scaling to z score
        # Hint: tft.scale_to_z_score
        features_dict[_transformed_name(feature)] = tft.scale_to_z_score(data_col)

    for feature in _VOCAB_FEATURE_KEYS:
        data_col = inputs[feature]         
        # Transform using vocabulary available in column
        # Hint: Use tft.compute_and_apply_vocabulary
        features_dict[_transformed_name(feature)] = tft.compute_and_apply_vocabulary(data_col)

    for feature in _HASH_STRING_FEATURE_KEYS:
        data_col = inputs[feature]         
        # Transform by hashing strings into buckets
        # Hint: Use tft.hash_strings with the param hash_buckets set to 10
        features_dict[_transformed_name(feature)] = tft.hash_strings(data_col, hash_buckets = 10)
    
    ### END CODE HERE ###  

    # No change in the label
    features_dict[_LABEL_KEY] = inputs[_LABEL_KEY]

    return features_dict
