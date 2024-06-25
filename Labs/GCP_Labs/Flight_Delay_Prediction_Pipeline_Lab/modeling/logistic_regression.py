import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
import warnings

warnings.filterwarnings("ignore")
import pickle
from google.cloud import storage

# Data Loading
df = pd.read_csv('cleaned.csv')

# Encode the target variable
le = LabelEncoder()
df['FLIGHT_STATUS'] = le.fit_transform(df['FLIGHT_STATUS'])

# Define features (X) and target (y)
y = df['FLIGHT_STATUS']
X = df.drop(['FLIGHT_STATUS', 'DEP_DELAY'], axis=1)

# Identify categorical and numerical columns
categorical_cols = ['OP_CARRIER', 'ORIGIN', 'DEST']
numerical_cols = X.columns.difference(categorical_cols)

# Preprocessing pipelines for both numerical and categorical data
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols),
    ]
)

# Apply the transformations to the features
X_preprocessed = preprocessor.fit_transform(X)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_preprocessed, y, test_size=0.25, random_state=42
)

# Train the Logistic Regression model
clf = LogisticRegression(max_iter=1000, n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)
training_preds = clf.predict(X_train)
val_preds = clf.predict(X_test)
training_accuracy = accuracy_score(y_train, training_preds)
val_accuracy = accuracy_score(y_test, val_preds)

print("Training Accuracy: {:.2f}%".format(training_accuracy * 100))
print("Validation Accuracy: {:.2f}%".format(val_accuracy * 100))

print("Confusion Matrix:\n", confusion_matrix(y_test, val_preds))
print("Classification Report:\n", classification_report(y_test, val_preds))

# Save the model and the preprocessor to disk
with open('model.pkl', 'wb') as model_file:
    pickle.dump(clf, model_file)

with open('preprocessorlr.pkl', 'wb') as preprocessor_file:
    pickle.dump(preprocessor, preprocessor_file)


# Upload the files to GCS
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


bucket_name = 'final-lab-model-bucket'
upload_to_gcs(bucket_name, 'model.pkl', 'models/model.pkl')
upload_to_gcs(bucket_name, 'preprocessorlr.pkl', 'models/preprocessorlr.pkl')

print("Model and preprocessor saved")
