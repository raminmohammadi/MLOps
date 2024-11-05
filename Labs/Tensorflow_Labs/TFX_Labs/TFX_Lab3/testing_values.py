import tensorflow as tf

raw_data = [
    {
        "Elevation": 2596,
        "Slope": 3,
        "Horizontal_Distance_To_Hydrology": 258,
        "Vertical_Distance_To_Hydrology": 0,
        "Horizontal_Distance_To_Roadways": 510,
        "Hillshade_9am": 221,
        "Hillshade_Noon": 232,
        "Horizontal_Distance_To_Fire_Points": 6279,
        "Wilderness_Area": "Rawah",
        "Soil_Type": "C7745",
        "Cover_Type": 4,
    }
]

feature_description = {
    "Elevation": tf.io.FixedLenFeature([], tf.int64),
    "Slope": tf.io.FixedLenFeature([], tf.int64),
    "Horizontal_Distance_To_Hydrology": tf.io.FixedLenFeature([], tf.int64),
    "Vertical_Distance_To_Hydrology": tf.io.FixedLenFeature([], tf.int64),
    "Horizontal_Distance_To_Roadways": tf.io.FixedLenFeature([], tf.int64),
    "Hillshade_9am": tf.io.FixedLenFeature([], tf.int64),
    "Hillshade_Noon": tf.io.FixedLenFeature([], tf.int64),
    "Horizontal_Distance_To_Fire_Points": tf.io.FixedLenFeature([], tf.int64),
    "Wilderness_Area": tf.io.FixedLenFeature([], tf.string),
    "Soil_Type": tf.io.FixedLenFeature([], tf.string),
    "Cover_Type": tf.io.FixedLenFeature([], tf.int64),
}
