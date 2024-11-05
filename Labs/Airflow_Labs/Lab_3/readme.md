Here’s a complete guide to setting up, deploying, and triggering Apache Airflow DAGs from a virtual machine (VM). This includes creating an Airflow environment, configuring the API, organizing the folder structure, and setting up DAGs to run a sample Python script.

---

## Step-by-Step Guide: Deploying and Triggering Airflow DAGs on a VM

### 1. Create and Configure a VM
1. **Create a Virtual Machine Instance**:
   - Log in to your cloud provider and create a new VM instance with sufficient resources (e.g., 2 vCPUs, 4GB RAM) to handle Airflow.

2. **Set Up Networking**:
   - Go to **VPC Network** and add a firewall rule to allow HTTP (port 80) and custom Airflow webserver port (e.g., port 8080).

---

### 2. Update and Install Necessary Packages
After the VM is set up, SSH into it and update the system, then install necessary packages:
```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-full -y
```

### 3. Set Up a Virtual Environment for Airflow
1. **Create a Virtual Environment**:
   ```bash
   python3 -m venv airflow_new_venv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source airflow_new_venv/bin/activate
   ```

3. **Install Apache Airflow**:
   ```bash
   pip install apache-airflow
   ```

4. **Initialize the Airflow Database**:
   ```bash
   airflow db init
   ```

---

### 4. Start the Airflow Webserver and Scheduler
To start Airflow, open two separate terminals and activate the virtual environment in each:

1. **Terminal 1**: Start the Webserver
   ```bash
   source airflow_new_venv/bin/activate
   airflow webserver --port 8080
   ```

2. **Terminal 2**: Start the Scheduler
   ```bash
   source airflow_new_venv/bin/activate
   airflow scheduler
   ```

The Airflow web interface should now be accessible at `http://<VM-IP>:8080`.

---

### 5. Enable the Airflow API
To enable the Airflow API, configure the `airflow.cfg` file:
1. Open the `airflow.cfg` file for editing:
   ```bash
   nano ~/airflow/airflow.cfg
   ```
2. Locate the `[api]` section and modify it to enable the API:
   ```ini
   [api]
   auth_backend = airflow.api.auth.backend.basic_auth
   ```

### 6. Create an Airflow Admin User
To authenticate with the API, create a user:
```bash
airflow users create \
  --username triggerdag \
  --firstname Rahul \
  --lastname Odedra \
  --role Admin \
  --email mlops.fall.2024@gmail.com
```

---

### 7. Set Up Folder Structure for Airflow Project
1. In your Airflow directory, create folders for DAGs and requirements:
   ```bash
   mkdir dags
   mkdir dags/src
   touch requirements.txt
   ```

2. **Add Python Scripts for DAGs**:
   - Place your DAG Python script, `my_dag.py`, in the `dags` folder.
   - Place other required scripts, like `model_development.py` and `success_email.py`, in the `dags/src` folder.

   Example structure:
   ```plaintext
   airflow/
   ├── dags/
   │   ├── my_dag.py
   │   └── src/
   │       ├── model_development.py
   │       └── success_email.py
   └── requirements.txt
   ```

---

### 8. Create and Edit DAG Files

1. **Define DAG**:
   Create and edit the `my_dag.py` DAG file:
   ```bash
   nano dags/my_dag.py
   ```

   Sample `my_dag.py` content:
   ```python
   from airflow import DAG
   from airflow.operators.python_operator import PythonOperator
   from datetime import datetime

   def sample_task():
       print("Executing the sample task.")

   with DAG('sample_dag', start_date=datetime(2023, 1, 1), schedule_interval='@daily', catchup=False) as dag:
       task1 = PythonOperator(
           task_id='sample_task',
           python_callable=sample_task
       )
   ```

2. **Additional Python Scripts**:
   Edit and add any additional scripts required, such as `model_development.py` and `success_email.py`.

---

### 9. Install Requirements
If you have any specific Python packages listed in `requirements.txt`, install them with:
```bash
pip install -r requirements.txt
```

---

### 10. Trigger the DAG
1. **Activate the Virtual Environment**:
   ```bash
   source airflow_new_venv/bin/activate
   ```

2. **Trigger the DAG Manually**:
   ```bash
   airflow dags trigger sample_dag
   ```

You should see logs confirming that the DAG `sample_dag` has been triggered. You can also monitor the DAG execution on the Airflow web interface.

---

### 11. Run and Test the DAG Locally
To test `my_dag.py` directly:
```bash
python3 dags/my_dag.py
```

This command will run the script locally and can help debug any issues before deploying it fully to Airflow.

---

### Recap of Key Commands
1. **Create Virtual Environment**:
   ```bash
   python3 -m venv airflow_new_venv
   source airflow_new_venv/bin/activate
   ```

2. **Initialize and Start Airflow**:
   ```bash
   airflow db init
   airflow webserver --port 8080
   airflow scheduler
   ```

3. **Trigger DAG**:
   ```bash
   airflow dags trigger sample_dag
   ```

Now your Airflow environment should be fully set up on the VM, with your DAG files organized and triggered successfully.