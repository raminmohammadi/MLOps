import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os


def load_data():
    """
    Loads data from a CSV file, serializes it, and returns the serialized data.

    Returns:
        bytes: Serialized data.
    """

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
    serialized_data = pickle.dumps(df)
    
    return serialized_data
    

def data_preprocessing(data):

    """
    Deserializes data, performs data preprocessing, and returns serialized clustered data.

    Args:
        data (bytes): Serialized data to be deserialized and processed.

    Returns:
        bytes: Serialized clustered data.
    """
    df = pickle.loads(data)
    df = df.dropna()
    clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]
    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return clustering_serialized_data


def build_save_model(data, filename):
    """
    Builds a KMeans clustering model, saves it to a file, and returns SSE values.

    Args:
        data (bytes): Serialized data for clustering.
        filename (str): Name of the file to save the clustering model.

    Returns:
        list: List of SSE (Sum of Squared Errors) values for different numbers of clusters.
    """
    df = pickle.loads(data)
    kmeans_kwargs = {"init": "random","n_init": 10,"max_iter": 300,"random_state": 42,}
    sse = []
    for k in range(1, 50):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)
    
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", filename)

    # Save the trained model to a file
    pickle.dump(kmeans, open(output_path, 'wb'))

    return sse


def load_model_elbow(filename,sse):
    """
    Loads a saved KMeans clustering model and determines the number of clusters using the elbow method.

    Args:
        filename (str): Name of the file containing the saved clustering model.
        sse (list): List of SSE values for different numbers of clusters.

    Returns:
        str: A string indicating the predicted cluster and the number of clusters based on the elbow method.
    """
    
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    # Load the saved model from a file
    loaded_model = pickle.load(open(output_path, 'rb'))

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test.csv"))
    
    kl = KneeLocator(
        range(1, 50), sse, curve="convex", direction="decreasing"
    )

    # Optimal clusters
    print(f"Optimal no. of clusters: {kl.elbow}")

    # Make predictions on the test data
    predictions = loaded_model.predict(df)
    
    return predictions[0]