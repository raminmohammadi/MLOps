"""Test script for train_and_save_model.py"""

import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from unittest.mock import patch, MagicMock
import sys
import os

# Append the directory above the current script directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.train_and_save_model import download_data, preprocess_data, train_model
from src.train_and_save_model import get_model_version, update_model_version
from src.train_and_save_model import ensure_folder_exists, save_model_to_gcs


# ----------------- Test Download ----------------- #
# Test the download_data function to ensure it correctly downloads and returns data
def test_download_data():
    X, y = download_data()
    
    # Check if the data is downloaded correctly and matches expected formats
    assert isinstance(X, pd.DataFrame)  # X should be a DataFrame
    assert isinstance(y, pd.Series)     # y should be a Series
    assert not X.empty                  # X should not be empty
    assert not y.empty                  # y should not be empty
    assert X.shape[0] == y.shape[0]     # The number of rows in X and y should be the same

# ----------------- Test Preprocess ----------------- #
# Test the preprocess_data function to ensure it correctly preprocesses the data
def test_preprocess_data():
    X, y = download_data()
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    
    # Assert that the preprocessing splits the data correctly
    assert X_train.shape[0] + X_test.shape[0] == X.shape[0]  # Rows in train and test should total original rows
    assert y_train.shape[0] + y_test.shape[0] == y.shape[0]  # Rows in train and test labels should total original labels
    assert X_train.shape[1] == X.shape[1]  # Number of features should remain the same

# ----------------- Test Train model ----------------- #
# Test the train_model function to ensure it correctly trains the model
def test_train_model():
    # Generate sample data for testing
    X = pd.DataFrame({
        'sepal length (cm)': [5.1, 4.9, 4.7, 4.6, 5.0],
        'sepal width (cm)': [3.5, 3.0, 3.2, 3.1, 3.6],
        'petal length (cm)': [1.4, 1.4, 1.3, 1.5, 1.4],
        'petal width (cm)': [0.2, 0.2, 0.2, 0.2, 0.2],
    })
    y = pd.Series([0, 0, 0, 0, 0])
    
    # Train the model using the sample data
    model = train_model(X, y)
    
    # Assertions to verify the model is trained correctly
    assert isinstance(model, RandomForestClassifier)  # Check if the returned model is of the correct type
    assert hasattr(model, 'predict')                  # Ensure the model has a predict method

# ----------------- Test Model versioning ----------------- #
# This function tests the get_model_version function responsible for retrieving the version of the model stored in Google Cloud Storage.
def test_get_model_version():
    # Patch the GCP storage client to prevent actual network operations during the test.
    with patch('train_and_save_model.storage.Client') as mock_storage_client:
        mock_bucket = MagicMock()  # Create a mock bucket object.
        mock_blob = MagicMock()    # Create a mock blob object to represent the file in the storage.

        # Configure mock objects to return other mocks when methods are called.
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        # Set the test inputs for actual function calls
        bucket_name = "bucket-test"
        version_file_name = "version.txt"

        # Simulate the scenario where the version file exists in the storage
        mock_blob.exists.return_value = True
        version = get_model_version(bucket_name, version_file_name)
        mock_blob.download_as_text.return_value = '1'  # Simulate blob returning version '1' as text

        # Check if the correct version is retrieved and the corresponding methods are called on the mock
        assert version == 1
        mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
        mock_bucket.blob.assert_called_once_with(version_file_name)
        mock_blob.download_as_text.assert_called_once()
        
        # Reset mocks to clear call history before the next test
        mock_storage_client.reset_mock()
        mock_bucket.reset_mock()
        mock_blob.reset_mock()
        
        # Test scenario where the version file does not exist
        mock_blob.exists.return_value = False
        version = get_model_version(bucket_name, version_file_name)
        mock_blob.download_as_text.return_value = '0'  # No file to download, should return 0

        # Ensure it handles the absence of the version file correctly
        assert version == 0
        mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
        mock_bucket.blob.assert_called_once_with(version_file_name)
        mock_blob.download_as_text.assert_not_called()

# ----------------- Test Update Model version ----------------- #
# This function tests the update_model_version function that updates the version of the model stored in Google Cloud Storage.
def test_update_model_version():
    # Patch the GCP storage client to prevent actual network operations during the test.
    with patch('train_and_save_model.storage.Client') as mock_storage_client:
        mock_bucket = MagicMock()  # Create a mock bucket object.
        mock_blob = MagicMock()    # Create a mock blob object to represent the file in the storage.

        # Configure mock objects to return other mocks when methods are called.
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        bucket_name = 'bucket-test'
        version_file_name = 'version.txt'
        new_version = 2
        
        # Test successful update of the model version
        result = update_model_version(bucket_name, version_file_name, new_version)
        # Assert the function returns true indicating success
        assert result == True
        mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
        mock_bucket.blob.assert_called_once_with(version_file_name)
        mock_blob.upload_from_string.assert_called_once_with(str(new_version))
        
        # Reset mocks to clear call history for further tests
        mock_storage_client.reset_mock()
        mock_bucket.reset_mock()
        mock_blob.reset_mock()
        
        # Test error handling with an invalid version (not an integer)
        with pytest.raises(ValueError):
            update_model_version(bucket_name, version_file_name, 'invalid_version')
        
        # Simulate an exception during the blob upload to test error handling
        mock_blob.upload_from_string.side_effect = Exception("Upload failed")
        result = update_model_version(bucket_name, version_file_name, new_version)
        # Assert the function returns false indicating failure
        assert result == False
        mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
        mock_bucket.blob.assert_called_once_with(version_file_name)
        mock_blob.upload_from_string.assert_called_once_with(str(new_version))


# ----------------- Test Ensure Folder Exists ----------------- #
# Test ensure_folder_exists function to verify it correctly ensures the presence of a folder in the storage
def test_ensure_folder_exists():
    with patch('train_and_save_model.storage.Client') as mock_storage_client:
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        folder_name = "trained_models"
        
        # When folder does not exist
        mock_blob.exists.return_value = False
        ensure_folder_exists(mock_bucket, folder_name)
        mock_bucket.blob.assert_called_with(f"{folder_name}/")
        mock_blob.upload_from_string.assert_called_once_with('')
        
        # Reset the mock for the next test
        mock_blob.reset_mock()
        
        # When folder exists
        mock_blob.exists.return_value = True
        ensure_folder_exists(mock_bucket, folder_name)
        mock_bucket.blob.assert_called_with(f"{folder_name}/")
        mock_blob.upload_from_string.assert_not_called()

# ----------------- Test Save model to GCS ----------------- #
# Test save_model_to_gcs function to ensure it saves the model to Google Cloud Storage correctly
def test_save_model_to_gcs():
    # Create a mock model for testing
    model = RandomForestClassifier()
    
    # Set up a patch context manager for storage.Client to mock GCS interactions
    with patch('train_and_save_model.storage.Client') as mock_storage_client:
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        
        # Define mock bucket and blob objects using a chain of return values
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        
        # Set the exists value on mock blob to return False
        mock_blob.exists.return_value = False
        
        # Call save_model_to_gcs with mock objects and check method calls
        save_model_to_gcs(model, 'bucket-test', 'blob-test')
        
        mock_storage_client.assert_called_once()
        mock_storage_client.return_value.bucket.assert_called_once_with('bucket-test')
        
        assert mock_bucket.blob.call_count == 2
        mock_bucket.blob.assert_any_call('trained_models/')
        mock_bucket.blob.assert_any_call('blob-test')
        mock_blob.upload_from_filename.assert_called_once_with('model.joblib')
