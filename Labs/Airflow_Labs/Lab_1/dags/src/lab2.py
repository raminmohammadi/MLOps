from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import pickle
import os

def load_cali_data():
    """
    Loads data from sklearn, serializes it, and returns the serialized data.

    Returns:
        bytes: Serialized data.
    """

    data = fetch_california_housing(as_frame = True).frame
    serialized_data = pickle.dumps(data)

    return serialized_data


def cali_data_preprocessing(data):
    """
    Deserializes data, performs data preprocessing

    Args:
        data (bytes): Serialized data to be deserialized and processed.

    Returns:
        bytes: Serialized processed data
    """

    df = pickle.loads(data)
    df = df.dropna()
    # Considering only a portion of teh dataset (4000 from 20000)
    sample_df = df.sample(n = 4000, random_state = 42).reset_index(drop=True)

    selected_features = ['MedInc', 'HouseAge', 'AveRooms', 'Population', 'MedHouseVal']
    selected_df = sample_df[selected_features]

    min_max_scaler = MinMaxScaler()
    data_minmax = min_max_scaler.fit_transform(selected_df)
    serialized_data_minmax = pickle.dumps(data_minmax)
    return serialized_data_minmax


def build_save_cali_model(cluster_count, data, filename):
    """
    Builds a KMeans clustering model, saves it to a file, and returns SSE value.

    Args:
        data (bytes): Serialized data for clustering.
        filename (str): Name of the file to save the clustering model.

    Returns:
        float : SSE (Sum of Squared Errors) values for different provided of clusters.
    """
    df = pickle.loads(data)
    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}

    kmeans = KMeans(n_clusters=cluster_count, **kmeans_kwargs)
    kmeans.fit(df)

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    # Create the model directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, filename)

    # Save the trained model to a file
    with open(output_path, 'wb') as f:
        pickle.dump(kmeans, f)

    return kmeans.inertia_



