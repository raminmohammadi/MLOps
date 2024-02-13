import random
import numpy as np
from sklearn import model_selection, datasets, preprocessing
from sklearn.linear_model import LogisticRegression
import calculator
import pickle


def generate_random_data():
    """
    Generate random synthetic data with two clusters.
    
    :return: 
    X (array-like): The generated data points with shape (n_samples, n_features).
    y (array-like): The labels associated with the data points, where each label
                    indicates the cluster to which the corresponding data point belongs.
    """
    X, y = datasets.make_blobs(n_samples=1000, n_features=4, centers=2)
    return X, y


def data_preprocessing(X, y, test_size=0.33, seed=7):
    """
    Preprocesses the input data for machine learning.

    Splits the input data into training and testing sets.
    
    :param X: The feature matrix of shape (n_samples, n_features).
    :param y: The target vector of shape (n_samples,).
    :param test_size: The proportion of the data to include in the test split. Default is 0.33.
    :param seed: The random seed for reproducibility. Default is 7.
    
    :return:
    X_train_minmax (array-like): The scaled feature matrix for the training set.
    y_train (array-like): The target vector for the training set.
    X_test_minmax (array-like): The scaled feature matrix for the test set.
    y_test (array-like): The target vector for the test set.

    
    """
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=test_size, random_state=seed)
    return X_train, y_train, X_test, y_test


def build_save_model(filename, X, y):
    """
    Builds a logistic regression model, fits it to the input data, and saves the trained model to a file.

    Args:
        filename (str): The name of the file where the trained model will be saved.
        X (array_like): The feature matrix of shape (n_samples, n_features).
        y (array_like): The target vector of shape (n_samples,).
    """
    # sample filename = 'finalized_model.sav'
    model = LogisticRegression(solver='lbfgs', max_iter=100)
    model.fit(X, y)
    pickle.dump(model, open(filename, 'wb'))


def load_model(filename):
    """
    Loads a saved machine learning model from a file using pickle.

    Args:
        filename (str): The name of the file containing the saved model.

    Returns:
        object: The loaded machine learning model.
    """

    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model


def predict(input_x, model):
    """
    Makes a prediction using a trained machine learning model.

    Args:
        input_x (array-like): The input data point or feature vector for prediction.
        model (object): The trained machine learning model used for prediction.

    Returns:
        int: The cluster to which it belongs.
    """
    return model.predict([input_x])[0]


def scale_input(data):
    """
    Scale the input data to a range between 0 and 1.

    :param data: NumPy array or list
        The input data to be scaled.

    :return: NumPy array
        The scaled data.
    """
    return np.clip(data, 0, 1)


def main():
    X, y = generate_random_data()
    X = scale_input(X)
    X_train, y_train, X_test, y_test = data_preprocessing(X, y)
    build_save_model("finalized_model.sav", X_train, y_train)
    model = load_model("finalized_model.sav")
    a = random.random()
    b = random.random()
    l = []
    l.append(calculator.fun1(a, b))
    l.append(calculator.fun2(a, b))
    l.append(calculator.fun3(a, b))
    l.append(calculator.fun4(l[0], l[1], l[2]))
    l = np.array(l)
    input = scale_input(l)
    return predict(input, model)


if __name__ == "__main__":
    print(main())
