import joblib
import logging

logger = logging.getLogger(__name__)


def predict_data(X):
    """
    Predict the class labels for the input data.
    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
    Returns:
        y_pred (numpy.ndarray): Predicted class labels.
    """
    try:
        logger.debug(f"Loading model for prediction.....")
        model = joblib.load("../model/penguin_model.pkl")
        logger.debug(f"Input Shape : {X.shape}")
        y_pred = model.predict(X)
        logger.debug(f"prediction resut : {y_pred}")
        return y_pred
    except Exception as e:
        logger.error(f"Error in perdict_data function: {str(e)}")
        raise
