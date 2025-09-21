import joblib


def predict_dt(X):
    """
    Predict the class labels for the input data using
    a Decision Tree classifier.

    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
                           Shape should be (n_samples, n_features).

    Returns:
        numpy.ndarray: Predicted class labels as integers.
    """
    model = joblib.load("../model/iris_model_dt.pkl")
    return model.predict(X)


def predict_rf(X):
    """
    Predict the class labels for the input data using
    a Random Forest classifier.

    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
                           Shape should be (n_samples, n_features).

    Returns:
        numpy.ndarray: Predicted class labels as integers.
    """
    model = joblib.load("../model/iris_model_rf.pkl")
    return model.predict(X)


def predict_lr(X):
    """
    Predict the class labels for the input data using
    a Logistic Regression model.

    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
                           Shape should be (n_samples, n_features).

    Returns:
        numpy.ndarray: Predicted class labels as integers.
    """
    model = joblib.load("../model/iris_model_lr.pkl")
    return model.predict(X)
