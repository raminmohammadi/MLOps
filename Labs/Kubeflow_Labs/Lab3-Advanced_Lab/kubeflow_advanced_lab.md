
# Advanced Kubeflow Lab: Credit Risk Classification Pipeline
---
In this lab we will create a pipeline on Kubeflow for credit risk classification. Using the **Credit Risk Dataset** as input.
- Data loading and augmentation
- Data preprocessing
- Model training with **XGBoost**
- Model conversion for optimized inference
- Model evaluation and metric logging
- Visualization of the ROC curve

## Dataset and Model Details

### Input Dataset: Credit Risk Dataset
The pipeline uses a **Credit Risk Dataset**, which contains information on loan applicants, including demographic details, financial attributes, and loan details. The dataset includes columns such as:
- `person_age`: Age of the loan applicant.
- `person_income`: Income level of the loan applicant.
- `person_home_ownership`: Type of home ownership.
- `loan_intent`: The purpose of the loan.
- `loan_grade`: A grading metric for the loan.
- `loan_amnt`: The amount requested for the loan.
- `loan_int_rate`: The interest rate of the loan.
- `loan_status`: Target variable indicating whether the applicant defaulted (1) or not (0).

### Model: XGBoost Classifier
The primary model used in this pipeline is **XGBoost**, a popular gradient-boosting algorithm. It is known for its efficiency and performance in structured/tabular data tasks. XGBoost parameters are customized in this pipeline to optimize for binary classification, specifically predicting the likelihood of loan default. After training, the model is converted to **daal4py**, an inference-optimized format, to speed up predictions.

## Pipeline Components

### 1. `load_data` Component

**Purpose**: Downloads a dataset from a specified URL, augments it with synthetic data, and saves it as an output artifact.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["numpy", "pandas", "loguru"])
def load_data(data_url: str, data_size: int, credit_risk_dataset: Output[Dataset]):
```

- **Parameters**:
  - `data_url`: URL where the dataset is hosted.
  - `data_size`: Desired size.

This component:
1. Downloads a credit risk dataset.
2. Expands the dataset with synthetic data by duplicating and perturbing columns.
3. Saves the modified dataset as `credit_risk_dataset` for downstream components.


### 2. `create_train_test_set` Component

**Purpose**: Splits the dataset into training (75%) and test (25%) sets.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas", "scikit-learn", "loguru"])
def create_train_test_set(data: Input[Dataset], x_train_data: Output[Dataset], y_train_data: Output[Dataset], x_test_data: Output[Dataset], y_test_data: Output[Dataset]):
```

- **Inputs**: 
  - `data`: The augmented dataset from `load_data`.
- **Outputs**:
  - `x_train_data`, `y_train_data`: Training features and labels.
  - `x_test_data`, `y_test_data`: Testing features and labels.

### 3. `preprocess_features` Component

**Purpose**: Preprocesses and scales data for model training.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas", "scikit-learn"])
def preprocess_features(x_train: Input[Dataset], x_test: Input[Dataset], x_train_processed: Output[Dataset], x_test_processed: Output[Dataset]):
```

This component applies data transformations using `ColumnTransformer` and `Pipeline` from Scikit-Learn:
- **Numerical features**: Imputation and scaling.
- **Categorical features**: One-hot encoding.

### 4. `train_xgboost_model` Component

**Purpose**: Trains an XGBoost model on the preprocessed data.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["pandas", "xgboost", "joblib", "loguru"])
def train_xgboost_model(x_train: Input[Dataset], y_train: Input[Dataset], xgb_model: Output[Model]):
```

- **Inputs**: 
  - Processed training data from `preprocess_features`.
- **Outputs**:
  - `xgb_model`: Trained XGBoost model.

### 5. `convert_xgboost_to_daal4py` Component

**Purpose**: Converts the XGBoost model to `daal4py` format, optimized for faster inference.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["daal4py", "joblib", "loguru", "scikit-learn"])
def convert_xgboost_to_daal4py(xgb_model: Input[Model], daal4py_model: Output[Model]):
```

This component:
1. Loads the trained XGBoost model.
2. Converts it to an optimized `daal4py` model using `daal4py` library.
3. Saves the converted model as `daal4py_model`.

### 6. `daal4py_inference` Component

**Purpose**: Evaluates the `daal4py` model on test data, logging metrics like AUC and accuracy.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["daal4py", "pandas", "scikit-learn"])
def daal4py_inference(x_test: Input[Dataset], y_test: Input[Dataset], daal4py_model: Input[Model], prediction_data: Output[Dataset], report: Output[Dataset], metrics: Output[Metrics]):
```

### 7. `plot_roc_curve` Component

**Purpose**: Plots the ROC curve based on model predictions.

```python
@dsl.component(
    base_image="python:3.10",
    packages_to_install=["numpy", "pandas", "scikit-learn"])
def plot_roc_curve(predictions: Input[Dataset], class_metrics: Output[ClassificationMetrics]):
```

This component:
1. Loads true labels and predicted probabilities from `daal4py_inference`.
2. Computes false positive and true positive rates to plot the ROC curve.
3. Logs the ROC curve using Kubeflow’s `ClassificationMetrics`.

## Main Pipeline: `model_pipeline`

```python
@dsl.pipeline
def model_pipeline(data_url: str, data_size: int):
    load_data_op = load_data(data_url=data_url, data_size=data_size)
    create_train_test_set_op = create_train_test_set(data=load_data_op.outputs['credit_risk_dataset'])
    preprocess_features_op = preprocess_features(x_train=create_train_test_set_op.outputs['x_train_data'], x_test=create_train_test_set_op.outputs['x_test_data'])
    train_xgboost_model_op = train_xgboost_model(x_train=preprocess_features_op.outputs['x_train_processed'], y_train=create_train_test_set_op.outputs['y_train_data'])
    convert_xgboost_to_daal4py_op = convert_xgboost_to_daal4py(xgb_model=train_xgboost_model_op.outputs['xgb_model'])
    daal4py_inference_op = daal4py_inference(x_test=preprocess_features_op.outputs['x_test_processed'], y_test=create_train_test_set_op.outputs['y_test_data'], daal4py_model=convert_xgboost_to_daal4py_op.outputs['daal4py_model'])
    plot_roc_curve_op = plot_roc_curve(predictions=daal4py_inference_op.outputs['prediction_data'])
```

- **Input Parameters**:
  - `data_url`: URL for the raw dataset.
  - `data_size`: Desired size for the augmented dataset.

Each component is linked sequentially, forming a pipeline where the output of one component is the input for the next.

## Compiling and Running the Pipeline

1. **Compile the Pipeline**:

    ```python
    if __name__ == '__main__':
        compiler.Compiler().compile(
            pipeline_func=model_pipeline,
            package_path='model_pipeline.yaml')
    ```

   Run this script to generate the `model_pipeline.yaml` file.

2. **Upload to Kubeflow**:
   - Open the Kubeflow Pipelines UI.
   - Click on “Upload pipeline” and select `model_pipeline.yaml`.
   - Upload the input data into a bucket and make it publicly accessible. Use this url as input to the model.
   - Provide the `data_url` and `data_size` as arguments when running the pipeline.

