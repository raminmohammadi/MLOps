# Airflow Lab Instructions and Description

## Introduction
This document provides a detailed breakdown of the two DAGs (`Airflow_Lab2` and `Airflow_Lab2_Flask`) along with explanations of each function within the DAG files. These explanations aim to clarify the purpose and functionality of each task and function in the Airflow workflows.


Watch the tutorial video for this lab at [Airflow Lab2 Tutorial Video](https://youtu.be/LwBFOyfN5TY)

## Prerequisites
Before proceeding with this lab, ensure the following prerequisites are met:

- Basic understanding of Apache Airflow concepts.
- Apache Airflow installed and configured.
- Necessary Python packages installed, including Flask.


## Airflow Email Configuration

### Sign in with app passwords
Follow the instruction provided here: [link](https://support.google.com/accounts/answer/185833) and get your smtp password

### Adding SMTP Information to airflow.cfg

To configure Airflow to send emails, you need to add SMTP information to the `airflow.cfg` file. Follow these steps:

1. Locate the `airflow.cfg` file in your Airflow installation directory.
2. Open the file using a text editor.
3. Search for the `[smtp]` section in the configuration file.
4. Update the following parameters with your SMTP server information:
   - `smtp_host`: Hostname of the SMTP server.
   - `smtp_starttls`: Set it to `True` if your SMTP server uses TLS.
   - `smtp_ssl`: Set it to `True` if your SMTP server uses SSL.
   - `smtp_user`: Your SMTP username.
   - `smtp_password`: Your SMTP password.
   - `smtp_port`: Port number of the SMTP server (e.g., 587 for TLS, 465 for SSL).
5. Save the changes to the `airflow.cfg` file.

for our lab assuming you have a gmail account you can use the following setting:
   - smtp_host = smtp.gmail.com
   - smtp_starttls = True
   - smtp_ssl = False
   - smtp_user = YOUREMAIL@gmail.com
   - smtp_password = Enter your password generated above
   - smtp_port = 587
   - smtp_mail_from = YOUREMAIL@gmail.com
   - smtp_timeout = 30
   - smtp_retry_limit = 5

After updating the SMTP information, Airflow will use the configured SMTP server to send email notifications.


## DAG Structure

### `Airflow_Lab2`
This DAG orchestrates a machine learning pipeline and notification system. Let's break down each function within this DAG:

1. **`notify_success(context)` and `notify_failure(context)` Functions:**
   - These functions define email notifications for task success and failure, respectively. They utilize the `EmailOperator` to send emails with predefined content and subject to a specified recipient (in this case, `rey.mhmmd@gmail.com`).

2. **`default_args` Dictionary:**
   - This dictionary defines default arguments for the DAG, including the start date and the number of retries in case of task failure.

3. **`dag` Definition:**
   - This section creates the main DAG instance (`Airflow_Lab2`) with various parameters such as description, schedule interval, catchup behavior, and tags.
   
4. **`owner_task` BashOperator:**
   - This task echoes `1` and is assigned to an owner (`Ramin Mohammadi`). It represents a simple demonstration task with a linked owner.

5. **`send_email` EmailOperator:**
   - This task sends a notification email upon DAG completion. It utilizes the `notify_success` and `notify_failure` functions as callbacks for success and failure, respectively.

6. **PythonOperator Tasks:**
   - These tasks execute Python functions (`load_data`, `data_preprocessing`, `separate_data_outputs`, `build_model`, `load_model`) representing different stages of a machine learning pipeline. They perform data loading, preprocessing, model building, and model loading tasks.

7. **`TriggerDagRunOperator` Task:**
   - This task triggers the `Airflow_Lab2_Flask` DAG upon successful completion of the main DAG. It ensures that the Flask API is launched after the machine learning pipeline completes successfully.

### `Airflow_Lab2_Flask`
This DAG manages the Flask API's lifecycle and consists of the following function:

1. **`check_dag_status()` Function:**
   - This function queries the status of the last DAG run (`Airflow_Lab2`). It returns `True` if the DAG run was successful, and `False` otherwise.

2. **`handle_api_request()` Function:**
   - This function handles API requests and redirects users to `/success` or `/failure` routes based on the status of the last DAG run.

3. **Flask Routes and HTML Templates:**
   - The Flask routes (`/api`, `/success`, `/failure`) define endpoints for accessing the API and displaying success or failure pages. These routes render HTML templates (`success.html`, `failure.html`) with appropriate messages.

4. **`start_flask_app()` Function:**
   - This function starts the Flask server, enabling users to access the API endpoints.

5. **`start_flask_API` PythonOperator:**
   - This task executes the `start_flask_app()` function to initiate the Flask server. It represents the starting point for the Flask API's lifecycle.

## Conclusion
In this project, we've constructed a robust workflow using Apache Airflow to orchestrate a machine learning pipeline and manage a Flask API for monitoring purposes. The Airflow_Lab2 DAG coordinates various tasks, including data loading, preprocessing, model building, and email notification upon completion. By leveraging PythonOperators and BashOperator, we've encapsulated each step of the machine learning process, allowing for easy scalability and maintenance.

Additionally, the integration of email notifications enhances the workflow's visibility, providing stakeholders with timely updates on task success or failure. This ensures proactive monitoring and quick response to any issues that may arise during pipeline execution.

Furthermore, the Airflow_Lab2_Flask DAG facilitates the management of a Flask API, enabling users to access endpoints for checking the status of the machine learning pipeline. By querying the last DAG run status, the API delivers real-time feedback, empowering users to make informed decisions based on the pipeline's performance.

Overall, this project demonstrates the power of Apache Airflow in orchestrating complex workflows and integrating external systems seamlessly. By following the provided instructions and understanding the workflow's structure, users can leverage Airflow to streamline their machine learning pipelines and enhance operational efficiency.

