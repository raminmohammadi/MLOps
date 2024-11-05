
# Hyperparameter Tuning with Kubeflow Katib

---

In this lab we will go through the process of hyperparameter tuning using **Kubeflow Katib**. We will optimize a **PyTorch MNIST** model by tuning its learning rate and momentum using Katib. The tuning will be performed by running multiple experiments to minimize the model's loss function.

## What is Katib?

**Katib** is a hyperparameter tuning tool integrated into **Kubeflow**. It allows you to automate the process of hyperparameter optimization for machine learning models. Katib can run parallel experiments, test various combinations of hyperparameters, and help identify the best-performing model configuration.

### Features:
- **Experiment Management:** Katib allows you to run multiple trials with different hyperparameter configurations.
- **Hyperparameter Search Algorithms:** Katib supports various algorithms like random search, grid search, and Bayesian optimization.
- **Scalability:** Since Katib is built for Kubernetes, it can efficiently scale across the cluster, running multiple trials in parallel.

### 1. MNIST Model Code

We will use a  **PyTorch MNIST** model for this lab. The model is trained to classify handwritten digits from the MNIST dataset. You can find the the code for the model (`mnist.py`), which will be used to perform hyperparameter tuning:


#### Building and Pushing the Docker Image

Before running the Katib experiment, we need to package the training code (`mnist.py`) into a Docker image, as Kubernetes (and Katib) uses containers to run jobs in an isolated, scalable manner. The Docker image provides all the dependencies and training code required to execute the trials.

#### Steps to Build and Push the Docker Image

1. **Create a Dockerfile**

   To containerize the `mnist.py` script, we create a `Dockerfile` that installs necessary dependencies and includes the Python script.


2. **Build the Docker Image**

   Run the following command from the directory containing your `Dockerfile` and `mnist.py` script to build the image:

   ```bash
   docker build -t <user-name>/<image-name>:<tag> .
   ```

   This command builds the Docker image and tags it as `<image-name>:<tag>`.

3. **Push the Docker Image to Docker Hub**

   After building the image, push it to Docker Hub to make it accessible from any Kubernetes cluster:

   ```bash
   docker push <user-name>/<image-name>:<tag>
   ```

   This step is critical since Katib needs to pull the image to run your training job on different nodes in the cluster.


### Why Containerize the Code for Tuning?

1. **Scalability:** Containers allow Katib to run multiple trials in parallel on different nodes in the Kubernetes cluster, ensuring efficient use of resources. Without containers, the code would need to be manually distributed to every node, which is both error-prone and time-consuming.

2. **Isolation:** Each trial runs in its own container, isolated from others. This prevents conflicts in dependencies, environments, or resource allocation that might arise when running multiple trials simultaneously.

3. **Portability:** Once the code is packaged into a Docker image, it can be run anywhere. The container ensures that the environment (e.g., Python version, libraries) is the same across different trials, reducing variability caused by inconsistent environments.

### 2. Create the Katib Experiment YAML

We will create a Katib experiment to run multiple trials with varying hyperparameter configurations (learning rate and momentum). Below is the configuration for the experiment:

```yaml
apiVersion: kubeflow.org/v1beta1
kind: Experiment
metadata:
  namespace: kubeflow
  name: firstexperiment
```
- **apiVersion:** This specifies the version of the Kubernetes resource you're creating (`kubeflow.org/v1beta1` for Katib experiments).
- **kind:** Defines the type of Kubernetes resource (`Experiment` for hyperparameter tuning).
- **metadata:** Contains metadata about the experiment.
  - **namespace:** Where the experiment runs (`kubeflow` in this case).
  - **name:** Name of the experiment (`firstexperiment`).

#### Objective Specification
```yaml
spec:
  objective:
    type: minimize
    goal: 0.001
    objectiveMetricName: loss
```
- **spec:** Contains the configuration for the experiment.
- **objective:** Defines what metric Katib will optimize.
  - **type:** Set to `minimize`, meaning Katib will aim to reduce the value of the metric.
  - **goal:** The target value for the metric (`0.001` for `loss`).
  - **objectiveMetricName:** Specifies the metric that Katib should monitor (`loss` in this case).

#### Search Algorithm
```yaml
  algorithm:
    algorithmName: random
```
- **algorithm:** Specifies the hyperparameter search algorithm.
  - **algorithmName:** Set to `random`, which randomly chooses hyperparameter values from the feasible space.

#### Parallelism and Trial Limits
```yaml
  parallelTrialCount: 3
  maxTrialCount: 12
  maxFailedTrialCount: 3
```
- **parallelTrialCount:** Defines how many trials will run in parallel (3 trials).
- **maxTrialCount:** Total number of trials Katib will run (12 trials).
- **maxFailedTrialCount:** Maximum number of allowed failed trials before Katib terminates the experiment (3 failures).

#### Hyperparameters
```yaml
  parameters:
    - name: lr
      parameterType: double
      feasibleSpace:
        min: "0.01"
        max: "0.05"
    - name: momentum
      parameterType: double
      feasibleSpace:
        min: "0.5"
        max: "0.9"
```
- **parameters:** Defines the hyperparameters to be tuned.
  - **name:** The hyperparameter name (`lr` for learning rate and `momentum` for momentum).
  - **parameterType:** Type of the hyperparameter (`double` means a floating-point number).
  - **feasibleSpace:** The range of values Katib can choose from for the hyperparameters.

### Trial Template
```yaml
  trialTemplate:
    primaryContainerName: training-container
    retain: true
    trialParameters:
      - name: learningRate
        description: Learning rate for the training model
        reference: lr
      - name: momentum
        description: Momentum for the training model
        reference: momentum
    trialSpec:
      apiVersion: batch/v1
      kind: Job
      spec:
        template:
          spec:
            containers:
              - name: training-container
                image: <user-name>/<image-name>:<tag>
                command:
                  - "python3"
                  - "/app/mnist.py"
                  - "--epochs=1"
                  - "--batch-size=16"
                  - "--lr=${trialParameters.learningRate}"
                  - "--momentum=${trialParameters.momentum}"
                resources:
                  limits:
                    memory: "1Gi"
                    cpu: "0.5"
            restartPolicy: Never
```
- **trialTemplate:** Specifies how each trial will be executed.
  - **primaryContainerName:** The container where the training happens (`training-container`).
  - **trialParameters:** Hyperparameters passed into the container for each trial.
    - **name:** The name of the parameter (e.g., `learningRate`, `momentum`).
    - **reference:** Refers to the corresponding hyperparameter in the `parameters` section (e.g., `lr`, `momentum`).

- **trialSpec:** Describes the Kubernetes Job that runs the trial.
  - **apiVersion** and **kind:** Defines the Kubernetes Job (`batch/v1`).
  - **containers:** Specifies the container for running the training job.
    - **image:** Docker image that contains the training code.
    - **command:** Command that runs the training script with the hyperparameters.
    - **resources:** Limits memory to `1Gi` and CPU to `0.5`.
  - **restartPolicy:** Set to `Never`, so the job will not restart if it fails.

---


### 3. Submitting the Experiment

We can submit the Katlib experiments in two ways. One is through CLI and another is through Kubeflow UI.
#### Submitting Katib Experiment via Kubeflow UI

- In the Kubeflow UI Dashboard,from the left-hand menu, click on AutoML (Katib).
- Inside the Experiments section: Create a New Experiment
- A form will appear where you can configure the experiment, but you can also directly edit the YAML file.
- Edit the YAML:
  - Paste the content from your experiment YAML file (katib-experiment.yaml)
- Save and Start the Experiment:
  - After pasting the YAML, click Submit to save and launch the experiment.
- The experiment will now run, and you can monitor its progress and results within the Katib Experiments section of the Kubeflow UI.

#### Submitting Katib Experiment via CLI

- Ensure you have your YAML file for the experiment saved.

- Run the following command to submit the experiment to Kubeflow:
  ```bash
  kubectl apply -f katib-experiment.yaml
  ```
  This command will apply the YAML configuration and trigger the Katib experiment. You can monitor the progress through the Kubeflow UI. 
### 4. Monitoring the Experiment

Katib will start running trials based on the configurations specified in the YAML file. You can monitor the experiment's progress on the **Kubeflow UI** or by querying Katib through the CLI.

### 5. Analyzing Results

Once the trials are complete, Katib will log the results, allowing you to identify the best-performing hyperparameters.

