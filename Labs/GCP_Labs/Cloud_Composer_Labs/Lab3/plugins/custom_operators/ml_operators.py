from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
import pickle
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class ModelDeployOperator(BaseOperator):
    """
    Custom Operator for deploying a machine learning model.
    """

    @apply_defaults
    def __init__(self, model_path, deployment_target, *args, **kwargs):
        super(ModelDeployOperator, self).__init__(*args, **kwargs)
        self.model_path = model_path
        self.deployment_target = deployment_target

    def execute(self, context):
        # Example deployment logic
        self.log.info(
            f"Deploying model from {self.model_path} to {self.deployment_target}"
        )

        # Deployment logic depends on the target platform
        if self.deployment_target == 'production':
            # Mock deployment code
            self.log.info("Model deployed to production.")
        else:
            self.log.info("Unsupported deployment target.")

        return f"Model deployed to {self.deployment_target} from {self.model_path}"


class MLModelTrainOperator(BaseOperator):
    """
    Custom Operator for training a machine learning model using pandas and scikit-learn.
    Allows for customization of hyperparameters and handles potential errors during training.
    """

    @apply_defaults
    def __init__(
        self,
        data_path,
        save_path,
        model_filename='model.pkl',  # Customizable model filename
        n_estimators=100,
        max_depth=None,
        random_state=42,
        test_size=0.2,  # Added test_size parameter
        *args,
        **kwargs,
    ):
        super(MLModelTrainOperator, self).__init__(*args, **kwargs)
        self.data_path = data_path
        self.save_path = save_path
        self.model_filename = model_filename
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.test_size = test_size

    def execute(self, context):
        try:
            # Load the dataset
            df = pd.read_csv(self.data_path)

            # Separate features (X) and target variable (y)
            X = df.drop("target", axis=1)  # Assuming 'target' is the label column
            y = df["target"]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.test_size, random_state=self.random_state
            )

            # Initialize and train the Random Forest model
            clf = RandomForestClassifier(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
            )
            clf.fit(X_train, y_train)

            # Construct the full path for saving the model
            model_filepath = os.path.join(self.save_path, self.model_filename)

            # Save the model to the specified path
            with open(model_filepath, 'wb') as file:
                pickle.dump(clf, file)

            self.log.info(f"Model successfully trained and saved to {model_filepath}")
            return model_filepath
        except Exception as e:
            self.log.error(f"Error during model training: {e}")
            raise
