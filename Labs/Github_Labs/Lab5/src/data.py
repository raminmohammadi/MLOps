import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

def load_data():
    """
    Load the Penguins dataset and return the features and target values.
    Returns:
        X (numpy.ndarray): The features of the Penguin dataset.
        y (numpy.ndarray): The target values of the Penguin dataset.
    """
    try:
        logger.info("Loading penguin dataset...")
        df = sns.load_dataset("penguins")
        features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
        df = df[features + ["species"]].dropna()

        logger.info(f"Dataset Loaded :  {len(df)} samples stored!")
        logger.debug(f"Features : {features}")

        X = df[features].to_numpy(dtype=float)
        y = df["species"].to_numpy()

        logger.info(f"Data Shape - X: {X.shape}, y : {y.shape}")
        return X, y
    except Exception as e:
        logger.error(f"Error with loading data : {str(e)}")
        raise

def split_data(X, y):
    """
    Split the data into training and testing sets.
    Args:
        X (numpy.ndarray): The features of the dataset.
        y (numpy.ndarray): The target values of the dataset.
    Returns:
        X_train, X_test, y_train, y_test (tuple): The split dataset.
    """
    try:
        logger.info("Splitting Data into Train and Test sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

        logger.info(f"Train set size: {X_train.shape[0]}, Test set size : {X_test.shape[0]}")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logger.error(f"Error Splitting Data : {str(e)}")
        raise
