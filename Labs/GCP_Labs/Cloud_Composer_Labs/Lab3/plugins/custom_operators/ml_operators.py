from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
import pickle
import os
from google.cloud import storage, aiplatform
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


class ModelDeployOperator(BaseOperator):
    """
    Custom Operator for deploying a machine learning model to GCS and Vertex AI.
    """

    @apply_defaults
    def __init__(
        self,
        model_directory,
        bucket_name,
        project_id,
        model_display_name,
        *args,
        **kwargs,
    ):
        super(ModelDeployOperator, self).__init__(*args, **kwargs)
        self.model_directory = model_directory
        self.bucket_name = bucket_name
        self.project_id = project_id
        self.model_display_name = model_display_name

    def execute(self, context):
        model_gcs_path = f"gs://{self.bucket_name}/{self.model_directory}"

        # Deploy the model to Vertex AI
        self.log.info(f"Deploying model to Vertex AI: {self.model_display_name}")

        aiplatform.init(project=self.project_id)

        try:
            model = aiplatform.Model.upload(
                display_name=self.model_display_name,
                artifact_uri=model_gcs_path,
                serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.0-24:latest',
            )
            self.log.info(
                f"Model successfully deployed to Vertex AI: {model.display_name}"
            )
            return model.resource_name
        except Exception as e:
            self.log.error(f"Failed to deploy model to Vertex AI: {e}")
            raise


class MLModelTrainOperator(BaseOperator):
    """
    Custom Operator for training a machine learning model using pandas and scikit-learn.
    Allows for customization of hyperparameters and handles potential errors during training.
    """

    @apply_defaults
    def __init__(
        self,
        data_path,
        bucket_name,  # GCS bucket name
        model_folder,  # Folder path within the bucket to save the model
        target_column,  # Added target_column parameter
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
        self.bucket_name = bucket_name  # GCS bucket name
        self.model_folder = (
            model_folder  # Folder path within the bucket to save the model
        )
        self.target_column = target_column  # Initialize target_column
        self.model_filename = model_filename
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.test_size = test_size

    def execute(self, context):
        try:
            # Load the dataset
            df = pd.read_csv(self.data_path)

            # Check if target_column exists in the dataframe
            if self.target_column not in df.columns:
                raise KeyError(
                    f"Target column '{self.target_column}' not found in the dataset."
                )

            # Separate features (X) and target variable (y)
            X = df.drop([self.target_column, 'Date'], axis=1)  # Exclude Date column
            y = df[self.target_column]

            # Ensure all features are numerical
            if not pd.api.types.is_numeric_dtype(y):
                raise ValueError(
                    f"Target column '{self.target_column}' must be numerical."
                )

            # Handle missing values
            X.fillna(X.mean(), inplace=True)

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.test_size, random_state=self.random_state
            )

            # Initialize and train the Random Forest model
            model = RandomForestRegressor(
                n_estimators=self.n_estimators,
                max_depth=self.max_depth,
                random_state=self.random_state,
            )
            model.fit(X_train, y_train)

            # Evaluate the model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            self.log.info(f"Model Mean Squared Error: {mse}")

            # Construct the full path for saving the model locally
            local_model_filepath = os.path.join('/tmp', self.model_filename)

            # Save the model to the specified local path
            with open(local_model_filepath, 'wb') as file:
                pickle.dump(model, file)

            self.log.info(
                f"Model successfully trained and saved locally to {local_model_filepath}"
            )

            # Upload the model to GCS
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(f'{self.model_folder}/{self.model_filename}')
            blob.upload_from_filename(local_model_filepath)

            self.log.info(
                f"Model successfully uploaded to gs://{self.bucket_name}/{self.model_folder}/{self.model_filename}"
            )

            return f"gs://{self.bucket_name}/{self.model_folder}/{self.model_filename}"
        except Exception as e:
            self.log.error(f"Error during model training: {e}")
            raise
