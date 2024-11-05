import tensorflow as tf

feature_description = {
    "holiday": tf.io.FixedLenFeature([], tf.string),
    "temp": tf.io.FixedLenFeature([], tf.float32),
    "rain_1h": tf.io.FixedLenFeature([], tf.float32),
    "snow_1h": tf.io.FixedLenFeature([], tf.float32),
    "clouds_all": tf.io.FixedLenFeature([], tf.int64),
    "weather_main": tf.io.FixedLenFeature([], tf.string),
    "weather_description": tf.io.FixedLenFeature([], tf.string),
    "date_time": tf.io.FixedLenFeature([], tf.string),
    "traffic_volume": tf.io.FixedLenFeature([], tf.int64),
    "month": tf.io.FixedLenFeature([], tf.int64),
    "day": tf.io.FixedLenFeature([], tf.int64),
    "day_of_week": tf.io.FixedLenFeature([], tf.int64),
    "hour": tf.io.FixedLenFeature([], tf.int64),
}

raw_data = [
    {
        "holiday": "None",
        "temp": 273.67,
        "rain_1h": 0.0,
        "snow_1h": 0.13,
        "clouds_all": 90,
        "weather_main": "Snow",
        "weather_description": "light snow",
        "date_time": "2016-01-08 15:00:00",
        "traffic_volume": 5548,
        "month": 1,
        "day": 8,
        "day_of_week": 4,
        "hour": 15,
    }
]