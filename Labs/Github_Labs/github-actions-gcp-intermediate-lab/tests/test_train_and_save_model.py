"""test script for train_and_save_model.py"""

import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from unittest.mock import patch, MagicMock
from train_and_save_model import download_data, preprocess_data, train_model
from train_and_save_model import get_model_version, update_model_version
from train_and_save_model import ensure_folder_exists, save_model_to_gcs


# ----------------- Test Download ----------------- #
# Test download_data function
def test_download_data():
  X, y = download_data()
  
  # Check if the data is downloaded correctly
  assert isinstance(X, pd.DataFrame)
  assert isinstance(y, pd.Series)
  assert not X.empty
  assert not y.empty
  assert X.shape[0] == y.shape[0]


# ----------------- Test Preprocess ----------------- #
# Test preprocess_data function
def test_preprocess_data():
  X, y = download_data()
  X_train, X_test, y_train, y_test = preprocess_data(X, y)
  
  assert X_train.shape[0] + X_test.shape[0] == X.shape[0]
  assert y_train.shape[0] + y_test.shape[0] == y.shape[0]
  assert X_train.shape[1] == X.shape[1]


# ----------------- Test Train model ----------------- #
# Test train_model function
def test_train_model():
  # Generate sample data
  X = pd.DataFrame({
    'sepal length (cm)': [5.1, 4.9, 4.7, 4.6, 5.0],
    'sepal width (cm)': [3.5, 3.0, 3.2, 3.1, 3.6],
    'petal length (cm)': [1.4, 1.4, 1.3, 1.5, 1.4],
    'petal width (cm)': [0.2, 0.2, 0.2, 0.2, 0.2],
  })
  
  y = pd.Series([0, 0, 0, 0, 0])
  
  model = train_model(X, y)
  
  # Assertions
  assert isinstance(model, RandomForestClassifier)
  assert hasattr(model, 'predict')


# ----------------- Test Model versioning ----------------- #
# Test get model version function
def test_get_model_version():
  with patch('train_and_save_model.storage.Client') as mock_storage_client:
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    # Test inputs for actual function
    bucket_name = "bucket-test"
    version_file_name = "version.txt"

    # When version file exists
    mock_blob.exists.return_value = True
    version = get_model_version(bucket_name, version_file_name)
    mock_blob.download_as_text.return_value = '1'
    # Assertions
    assert version == 1
    mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(version_file_name)
    mock_blob.download_as_text.assert_called_once()
    
    # Reset the mocks for the next test
    mock_storage_client.reset_mock()
    mock_bucket.reset_mock()
    mock_blob.reset_mock()
    
    # When version file does not exist
    mock_blob.exists.return_value = False
    version = get_model_version(bucket_name, version_file_name)
    mock_blob.download_as_text.return_value = '0'
    # Assertions
    assert version == 0
    mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(version_file_name)
    mock_blob.download_as_text.assert_not_called()
    

# ----------------- Test Update Model version ----------------- #
# Test update_model_version function
def test_update_model_version():
  with patch('train_and_save_model.storage.Client') as mock_storage_client:
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    bucket_name = 'bucket-test'
    version_file_name = 'version.txt'
    new_version = 2
    
    # Test successful update
    result = update_model_version(bucket_name, version_file_name, new_version)
    assert result == True
    mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(version_file_name)
    mock_blob.upload_from_string.assert_called_once_with(str(new_version))
    
    # Reset mocks
    mock_storage_client.reset_mock()
    mock_bucket.reset_mock()
    mock_blob.reset_mock()
    
    # Test invalid version
    with pytest.raises(ValueError):
      update_model_version(bucket_name, version_file_name, 'invalid_version')
      
    # Test exception handling scenario
    mock_blob.upload_from_string.side_effect = Exception("Upload failed")
    result = update_model_version(bucket_name, version_file_name, new_version)
    assert result == False
    mock_storage_client.return_value.bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(version_file_name)
    mock_blob.upload_from_string.assert_called_once_with(str(new_version))
  
  

# ----------------- Test Ensure Folder Exists ----------------- #
# Test function for ensure_folder_exists
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



# ----------------- Test Test and Save model to GCS ----------------- #
# Test save_model_to_gcs function
# For testing this function, since we are making calls to an external service (GCS)
# we need to mock GCS objects and client to prevent actual calls.
def test_save_model_to_gcs():
  # Create a mock model
  model = RandomForestClassifier()
  
  # Set up a patch context manager for storage.Client
  with patch('train_and_save_model.storage.Client') as mock_storage_client:
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    
    # Define mock bucket and blob objects using chain of return values
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    
    # Set the exists value on mock blob to return False
    mock_blob.exists.return_value = False
    
    # Call save_model_to_gcs with mock objects and check if the methods were called
    save_model_to_gcs(model, 'bucket-test', 'blob-test')
    
    mock_storage_client.assert_called_once()
    mock_storage_client.return_value.bucket.assert_called_once_with('bucket-test')
    
    assert mock_bucket.blob.call_count == 2
    mock_bucket.blob.assert_any_call('trained_models/')
    mock_bucket.blob.assert_any_call('blob-test')
    mock_blob.upload_from_filename.assert_called_once_with('model.joblib')
  
