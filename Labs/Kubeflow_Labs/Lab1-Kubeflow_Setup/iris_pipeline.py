import kfp
from kfp import dsl
from typing import NamedTuple
import subprocess


# Step 1: Load the Iris dataset
@dsl.component
def load_iris_data() -> NamedTuple('Outputs',
                                   [('X_train', list), ('X_test', list), ('y_train', list), ('y_test', list)]):
    import subprocess
    subprocess.run(['pip', 'install', 'scikit-learn', 'pandas'])

    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    import pandas as pd

    iris = load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training data: {X_train.shape}, Testing data: {X_test.shape}")

    return (X_train.tolist(), X_test.tolist(), y_train.tolist(), y_test.tolist())


# Step 2: Train a RandomForest classifier
@dsl.component
def train_model(X_train: list, X_test: list, y_train: list, y_test: list) -> float:
    import subprocess
    subprocess.run(['pip', 'install', 'scikit-learn', 'pandas'])

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    import numpy as np

    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

    return accuracy


@dsl.pipeline(
    name="Iris Classification Pipeline",
    description="Loads the Iris dataset and trains a RandomForest model"
)
def iris_pipeline():
    # Step 4: Load the Iris data
    data = load_iris_data()

    # Step 5: Train the model using the loaded data
    train_model(
        X_train=data.outputs['X_train'],
        X_test=data.outputs['X_test'],
        y_train=data.outputs['y_train'],
        y_test=data.outputs['y_test']
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(iris_pipeline, 'model_pipeline.yaml')