import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split

def load_data():
    """
    Load the Penguins dataset and return the features and target values.
    Returns:
        X (numpy.ndarray): The features of the Penguin dataset.
        y (numpy.ndarray): The target values of the Penguin dataset.
    """
    df = sns.load_dataset("penguins")
    features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    df = df[features + ["species"]].dropna()

    X = df[features].to_numpy(dtype=float)
    y = df["species"].to_numpy()
    return X, y

def split_data(X, y):
    """
    Split the data into training and testing sets.
    Args:
        X (numpy.ndarray): The features of the dataset.
        y (numpy.ndarray): The target values of the dataset.
    Returns:
        X_train, X_test, y_train, y_test (tuple): The split dataset.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test