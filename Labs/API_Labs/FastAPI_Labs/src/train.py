from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import joblib
from data import load_data, split_data


def fit_decision_tree(X_train, y_train):
    """
    Train a Decision Tree classifier on the Iris dataset
    and save the trained model as a pickle file.

    Args:
        X_train (numpy.ndarray): Training feature matrix of shape (n_samples, n_features).
        y_train (numpy.ndarray): Training target labels.

    Saves:
        ../model/iris_model_dt.pkl : Serialized Decision Tree model.
    """
    dt_classifier = DecisionTreeClassifier(max_depth=3, random_state=12)
    dt_classifier.fit(X_train, y_train)
    joblib.dump(dt_classifier, "../model/iris_model_dt.pkl")


def fit_random_forest(X_train, y_train):
    """
    Train a Random Forest classifier on the Iris dataset
    and save the trained model as a pickle file.

    Args:
        X_train (numpy.ndarray): Training feature matrix of shape (n_samples, n_features).
        y_train (numpy.ndarray): Training target labels.

    Saves:
        ../model/iris_model_rf.pkl : Serialized Random Forest model.
    """
    rf = RandomForestClassifier(n_estimators=100, random_state=12)
    rf.fit(X_train, y_train)
    joblib.dump(rf, "../model/iris_model_rf.pkl")


def fit_logistic_regression(X_train, y_train):
    """
    Train a Logistic Regression model on the Iris dataset
    and save the trained model as a pickle file.

    Args:
        X_train (numpy.ndarray): Training feature matrix of shape (n_samples, n_features).
        y_train (numpy.ndarray): Training target labels.

    Saves:
        ../model/iris_model_lr.pkl : Serialized Logistic Regression model.
    """
    lr = LogisticRegression(max_iter=200, random_state=12)
    lr.fit(X_train, y_train)
    joblib.dump(lr, "../model/iris_model_lr.pkl")


if __name__ == "__main__":
    """
    Script entry point for training all classifiers.
    Loads the Iris dataset, splits into train/test sets,
    and trains Decision Tree, Random Forest, and Logistic Regression models.
    """
    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    fit_decision_tree(X_train, y_train)
    fit_random_forest(X_train, y_train)
    fit_logistic_regression(X_train, y_train)

    print(" All models trained and saved in ../model/")
