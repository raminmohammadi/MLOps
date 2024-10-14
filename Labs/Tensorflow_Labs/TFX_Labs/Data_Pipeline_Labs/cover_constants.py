
SCALE_MINMAX_FEATURE_KEYS = [
        "Horizontal_Distance_To_Hydrology",
        "Vertical_Distance_To_Hydrology",
    ]

SCALE_01_FEATURE_KEYS = [
        "Hillshade_9am",
        "Hillshade_Noon",
        "Horizontal_Distance_To_Fire_Points",
    ]

SCALE_Z_FEATURE_KEYS = [
        "Elevation",
        "Slope",
        "Horizontal_Distance_To_Roadways",
    ]

VOCAB_FEATURE_KEYS = ["Wilderness_Area"]

HASH_STRING_FEATURE_KEYS = ["Soil_Type"]

LABEL_KEY = "Cover_Type"

# Utility function for renaming the feature
def transformed_name(key):
    return key + '_xf'
