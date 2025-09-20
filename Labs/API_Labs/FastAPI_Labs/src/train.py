from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.preprocessing import LabelEncoder
from data import load_data, split_data

def fit_model(X_train, y_train):
    """
    Train a Decision Tree Classifier and save the model to a file.
    Args:
        X_train (numpy.ndarray): Training features.
        y_train (numpy.ndarray): Training target values.
    """
    rf_classifier = RandomForestClassifier(max_depth=3, random_state=12)
    rf_classifier.fit(X_train, y_train)
    joblib.dump(rf_classifier, "../model/penguin_model.pkl")

if __name__ == "__main__":
    X, y = load_data()
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    X_train, X_test, y_train, y_test = split_data(X, y_enc)
    fit_model(X_train, y_train)
    artifact = {
        "classes": list(le.classes_)
    }
    joblib.dump(artifact, "../model/penguin_artifact.joblib")
