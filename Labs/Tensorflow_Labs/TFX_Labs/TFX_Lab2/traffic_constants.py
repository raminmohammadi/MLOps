
# Features to be scaled to the z-score
DENSE_FLOAT_FEATURE_KEYS = ['temp', 'snow_1h']

# Features to bucketize
BUCKET_FEATURE_KEYS = ['rain_1h']

# Number of buckets used by tf.transform for encoding each feature.
FEATURE_BUCKET_COUNT = {'rain_1h': 3}

# Feature to scale from 0 to 1
RANGE_FEATURE_KEYS = ['clouds_all']

# Number of vocabulary terms used for encoding VOCAB_FEATURES by tf.transform
VOCAB_SIZE = 1000

# Count of out-of-vocab buckets in which unrecognized VOCAB_FEATURES are hashed.
OOV_SIZE = 10

# Features with string data types that will be converted to indices
VOCAB_FEATURE_KEYS = [
    'holiday',
    'weather_main',
    'weather_description'
]

# Features with int data type that will be kept as is
CATEGORICAL_FEATURE_KEYS = [
    'hour', 'day', 'day_of_week', 'month'
]

# Feature to predict
VOLUME_KEY = 'traffic_volume'

def transformed_name(key):
    return key + '_xf'
