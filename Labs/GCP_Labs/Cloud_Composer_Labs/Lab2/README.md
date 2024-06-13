# Cloud Composer Intermediate Tutorial

This lab contains a Cloud Composer Intermediate tutorial that demonstrates various features of Apache Airflow including task parameterization, file operations, HTTP requests, task dependencies, and the use of sensors in GCP's Cloud Composer. The tutorial is structured into three Directed Acyclic Graphs (DAGs), each showcasing different functionalities.

Watch the tutorial video for this lab on our Youtube channel [tutorial Video](https://youtu.be/bvGipcGwtA8)

## Prerequisites

- Apache Airflow installed
- Google Cloud Storage (GCS) access with appropriate permissions
- Python 3.x
- Required Python packages: pandas, requests, apache-airflow, apache-airflow-providers-google


## DAGs Overview

### DAG 1: Parameterize File Path and Use FileSensor
- This DAG reads, processes a file, and uses a GCS File Sensor to detect the existence of a processed file.

Tasks
- read_and_serialize_task: Reads a CSV file from GCS, serializes it to JSON, and stores the result in XCom.
- process_task: Processes the serialized data from the previous task, fills missing values, and writes the output back to GCS.
- file_sensor_task: Waits for the processed file to appear in GCS, then logs the task completion status.

### DAG 2: File Operations and HTTP Request
This DAG performs file operations on GCS and makes an HTTP request.

Tasks
- file_op_task: Reads a file from GCS and logs its content.
- http_request_task: Makes an HTTP GET request to a given URL and logs the response.

### DAG 3: Task Dependencies
This DAG demonstrates task dependencies using dummy tasks, a bash command, and Python callable tasks.

Tasks
- start_task: Dummy task used to start the DAG.
- bash_task: Runs a simple bash command.
- middle_task: Logs a message indicating the task execution.
- branch_task: Dummy task used for branching logic.
- end_task: Logs a message indicating the task completion.

## Functions
`read_and_serialize`
Reads a CSV file from GCS, serializes it to JSON, and logs the content.

`read_and_serialize_return`
Wrapper function that returns the result of read_and_serialize

`process_file`
Processes the serialized data, fills missing values, and writes the output back to GCS.

`file_operation`
Reads a file from GCS and logs its content.

`make_http_request`
Makes an HTTP GET request to a specified URL and logs the response.

`log_file_sensor_output`
Logs the output of the file sensor task.

## How to Run
- Ensure Airflow is properly installed and configured.
- Place the Python script and required files in the appropriate directories.
- Trigger the DAGs using the Airflow UI or CLI.

```
airflow dags trigger dag_1_parameterize
airflow dags trigger dag_file_and_http
airflow dags trigger dag_3_dependencies
```


## Conclusion
This tutorial covers the basics of using Airflow with google cloud composer for various tasks such as file operations, HTTP requests, and demonstrating task dependencies. By following this tutorial, you should gain a good understanding of how to create and manage DAGs in Airflow.