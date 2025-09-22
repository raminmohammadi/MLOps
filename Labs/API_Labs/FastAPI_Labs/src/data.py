"""
data.py

Provides:
- load_data(): loads the Pima Indians Diabetes dataset (CSV) and returns X, y (numpy arrays).
- split_data(X, y): splits into train/test (default test_size=0.3, random_state=12).
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data() -> tuple:
    """
    Load the Pima Indians Diabetes dataset and perform basic preprocessing.
    Returns:
        X (np.ndarray): features
        y (np.ndarray): target
    """
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    columns = [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
    ]

    df = pd.read_csv(url, header=None, names=columns)

    # In this dataset, zeros in some columns indicate missing values.
    zero_invalid_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    # Replace zeros with NaN then fill with median of column
    df[zero_invalid_cols] = df[zero_invalid_cols].replace(0, np.nan)
    df[zero_invalid_cols] = df[zero_invalid_cols].fillna(df[zero_invalid_cols].median())

    X = df.drop("Outcome", axis=1).values
    y = df["Outcome"].values
    return X, y

def split_data(X, y, test_size: float = 0.3, random_state: int = 12):
    """
    Split dataset into train and test sets.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
