import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load New York City Airbnb dataset
data_url = "AB_NYC_2019.csv"
airbnb_data = pd.read_csv(data_url)

# Select features
features = ['latitude', 'longitude', 'minimum_nights', 'number_of_reviews', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365']

# Drop rows with missing values in selected features
cleaned_data = airbnb_data.dropna(subset=features)

# Split the dataset into features and target variable
X = cleaned_data[features]
y = cleaned_data['price']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestRegressor model
start_train_time = time.time()
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
end_train_time = time.time()

# Make predictions
start_pred_time = time.time()
predictions = model.predict(X_test)
end_pred_time = time.time()

# Calculate MSE
mse = mean_squared_error(y_test, predictions)

# Log timing metrics
print("Training Time: {:.2f} seconds".format(end_train_time - start_train_time))
print("Inference Time: {:.2f} seconds".format(end_pred_time - start_pred_time))
print("Mean Squared Error: {:.2f}".format(mse))
