import pandas as pd
import os
import pickle
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

# Load data from a CSV file
def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.

    Returns:
        bytes: Serialized data.
    """
    data = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/advertising.csv"))
    return data

# Preprocess the data
def data_preprocessing(data):
    X = data.drop(['Timestamp', 'Clicked on Ad', 'Ad Topic Line', 'Country', 'City'], axis=1)
    y = data['Clicked on Ad']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    num_columns = ['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage', 'Male']

    # Define a column transformer for preprocessing
    ct = make_column_transformer(
        (MinMaxScaler(), num_columns),
        (StandardScaler(), num_columns),
        remainder='passthrough'
    )

    # Transform the training and testing data
    X_train = ct.fit_transform(X_train)
    X_test = ct.transform(X_test)

    return X_train, X_test, y_train, y_test

# Build and save a logistic regression model
def build_model(data, filename):
    X_train, X_test, y_train, y_test = data

    # Define hyperparameter grid for grid search
    lr_clf = LogisticRegression()
    penalty = ['l1', 'l2']
    C = [0.5, 0.6, 0.7, 0.8]
    class_weight = [{1: 0.5, 0: 0.5}, {1: 0.4, 0: 0.6}, {1: 0.6, 0: 0.4}, {1: 0.7, 0: 0.3}]
    solver = ['liblinear', 'saga']

    param_grid = dict(
        penalty=penalty,
        C=C,
        class_weight=class_weight,
        solver=solver
    )

    # Create and train a logistic regression model with the best parameters
    lr_clf = LogisticRegression()
    lr_clf.fit(X_train, y_train)
    #output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", filename)
    # Save the trained model to a file
    pickle.dump(lr_clf, open(output_path, 'wb'))

# Load a saved logistic regression model and evaluate it
def load_model(data, filename):
    X_train, X_test, y_train, y_test = data
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    # Load the saved model from a file
    loaded_model = pickle.load(open(output_path, 'rb'))

    # Make predictions on the test data and print the model's score
    predictions = loaded_model.predict(X_test)
    print(f"Model score on test data: {loaded_model.score(X_test, y_test)}")

    return predictions[0]
