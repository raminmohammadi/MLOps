## Data Version Control (DVC)

- [DVC](https://dvc.org/) is an open-source tool that serves as a powerful asset in the machine learning project toolkit, with a primary focus on data versioning.
- **Data versioning** is a critical aspect of any ML project. It allows you to track changes and updates in your datasets over time, ensuring you can always recreate, compare, and reference specific dataset versions used in your experiments.
- In this lab tutorial, we will be utilizing DVC with Google Cloud Storage to enhance data versioning capabilities, ensuring efficient data management and collaboration within your machine learning project.


**top `dvc` commands** you’ll use day-to-day — grouped by purpose so you can navigate DVC confidently:

---

### 🚀 **1. Project Setup & Configuration**

| Command                                              | Purpose                                                        |
| ---------------------------------------------------- | -------------------------------------------------------------- |
| `dvc init`                                           | Initialize a new DVC repository (use `--no-scm` if no Git)     |
| `dvc remote add -d <name> <url>`                     | Add a remote storage (e.g., GCS, S3, Azure) and set as default |
| `dvc remote modify <name> credentialpath <key.json>` | Configure service account or credentials for remote            |
| `dvc config`                                         | Manage DVC configuration (local, global, or project-wide)      |

---

### 📦 **2. Data Tracking & Versioning**

| Command                         | Purpose                                                    |
| ------------------------------- | ---------------------------------------------------------- |
| `dvc add <data_file_or_dir>`    | Track a dataset or directory with DVC                      |
| `dvc remove <data_file_or_dir>` | Stop tracking a dataset                                    |
| `dvc move <old> <new>`          | Rename a tracked dataset while keeping metadata            |
| `dvc checkout`                  | Sync local workspace with the current version from Git/DVC |
| `dvc status`                    | Show changes in data, pipelines, or remote cache           |

---

### ☁️ **3. Storage & Syncing**

| Command     | Purpose                                                        |
| ----------- | -------------------------------------------------------------- |
| `dvc push`  | Upload data or model files to remote storage                   |
| `dvc pull`  | Download data or models from remote storage                    |
| `dvc fetch` | Download data dependencies (without putting them in workspace) |
| `dvc gc`    | Garbage collect unused cache or remote data                    |

---

### ⚙️ **4. Pipelines & Experiments**

| Command                                                | Purpose                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `dvc stage add -n <name> -d <input> -o <output> <cmd>` | Add a reproducible pipeline stage                                              |
| `dvc dag`                                              | Visualize the pipeline DAG (Directed Acyclic Graph)                            |
| `dvc exp run`                                          | Run experiments without committing changes                                     |
| `dvc exp show`                                         | Show experiment results in a table                                             |
| `dvc exp push/pull`                                    | Share or retrieve experiments                                                  |

---

### 📊 **5. Metrics, Params, and Plots**

| Command            | Purpose                                        |
| ------------------ | ---------------------------------------------- |
| `dvc metrics show` | Display tracked metrics (e.g., accuracy, loss) |
| `dvc metrics diff` | Compare metrics between commits or experiments |
| `dvc params diff`  | Show how parameters changed between commits    |
| `dvc plots diff`   | Visualize and compare performance over time    |

---

### 🔍 **6. Debugging & Info**

| Command           | Purpose                                                  |
| ----------------- | -------------------------------------------------------- |
| `dvc doctor`      | Diagnose environment issues                              |
| `dvc version`     | Show DVC version and dependencies                        |
| `dvc list <repo>` | List tracked files in a remote DVC repository            |
| `dvc diff`        | Show differences in DVC-tracked data between Git commits |

---

### 🧹 **7. Cleanup & Maintenance**

| Command                | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| `dvc destroy`          | Completely remove DVC from a project (undo `dvc init`) |
| `dvc unprotect <file>` | Remove DVC protection from a tracked file              |
| `dvc cache dir`        | Show or change cache directory location                |

---


### Creating a Google Cloud Storage Bucket
1. Navigate to [Google Cloud Console](https://console.cloud.google.com/).
2. Ensure you've created a new project specifically for this lab.
3. In the Navigation menu, select "Cloud Storage," then go to "Buckets," and click on "Create a new bucket."
4. Assign a unique name to your bucket.
5. Select the region as `us-east1`
6. Proceed by clicking "Continue" until your new bucket is successfully created.
7. Once the bucket is created, we need to get the credentials to connect the GCP remote to the project. Go to the `IAM & Admin` service and go to `Service Accounts` in the left sidebar.
8. Click the `Create Service Account` button to create a new service account that you'll use to connect to the DVC project in a bit. Now you can add the name and ID for this service account and keep all the default settings. We've chosen `lab2` for the name. Click `Create and Continue` and it will show the permissions settings. Select `Owner` in the dropdown and click `Continue` or select `storage.admin`.
9. Then add your user to have access to the service account and click `Done`. Finally, you'll be redirected to the `Service accounts` page. You’ll see your service account and you’ll be able to click on `Actions` and go to where you `Manage keys` for this service account. 
10. Once you’ve been redirected, click the `Add Key` button and this will bring up the credentials you need to authenticate your GCP account with your project. Proceed by downloading the credentials in JSON format and securely store the file. This file will serve as the authentication mechanism for DVC when connecting to Google Cloud.
### Installing DVC with Google Cloud Support
- Ensure you have DVC with Google Cloud support installed on your system by using the following command:
	`pip install dvc[gs]`
- Note that, depending on your chosen [remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage), you may need to install optional dependencies such as `[s3]`, `[azure]`, `[gdrive]`, `[gs]`, `[oss]`, `[ssh]`. To include all optional dependencies, use `[all]`.
- Run this command to setup google cloud bucket as your storage `dvc remote add -d myremote gs://<mybucket>`
- In order for DVC to be able to push and pull data from the remote, you need to have valid GCP credentials.
- Run the following command for authentication `dvc remote modify --lab2 credentialpath <YOUR JSON TOKEN LOCATION>`
### Tracking Data with DVC
- Ensure you have downloaded the [required data](https://www.kaggle.com/datasets/arjunbhasin2013/ccdata) and placed it in the "data" folder, renaming the file to "CC_GENERAL.csv."
- To initiate data tracking, execute the following steps:
	1. Run the `dvc init` command to initialize DVC for your project. This will generate a `.dvc` file that stores metadata and configuration details. Your `.dvc` file config metadata will look something like this
	```
    [core]
        remote = lab2
    ['remote "lab2"']
        url = gs://ie7374
	```

	dvc remote modify --git-action-gcp credentialpath git-action-gcp git-action-gcp-3e47dbac54ff.json 
	2. Next, use `dvc add data/CC_GENERAL.csv` to instruct DVC to start tracking this specific dataset.
	3. To ensure version control, add the generated `.dvc` file to your Git repository with `git add data/CC_GENERAL_csv.dvc`.
	4. Also, include the `.gitignore` file located in the "data" folder in your Git repository by running `git add data/.gitignore`.
	5. To complete the process, commit these changes with Git to record the dataset tracking configuration.

- To push your data to the remote storage in Google Cloud, use the following DVC command: `dvc push` This command will upload your data to the Google Cloud Storage bucket specified in your DVC configuration, making it accessible and versioned in the cloud.

### Handling Data Changes and Hash Updates
Whenever your dataset undergoes changes, DVC will automatically compute a new hash for the updated file. Here's how the process works:
- **Update the Dataset:** Replace the existing "CC_GENERAL.csv" file in the "data" folder with the updated version.
- **Update DVC Tracking:** Execute `dvc add data/CC_GENERAL.csv` again to update DVC with the new version of the dataset. When DVC computes the hash for the updated file, it will be different from the previous hash, reflecting the changes in the dataset.
- **Commit and Push:** Commit the changes with Git and push them to your Git repository. This records the update to the dataset, including the new hash.
- **Storage in Google Cloud:** When you run dvc push, DVC uploads the updated dataset to the Google Cloud Storage bucket specified in your DVC configuration. Each version of the dataset is stored as a distinct object within the bucket, organized for easy retrieval.
#### Reverting to Previous Versions with Hashes
To revert to a previous dataset version:
- **Checkout Git Commit:** Use Git to checkout the specific commit where the desired dataset version was last committed. For example, run `git checkout <commit-hash>`
- **Use DVC:** After checking out the Git commit, use DVC to retrieve the dataset version corresponding to that commit by running `dvc checkout`. DVC uses the stored hash to identify and fetch the correct dataset version associated with that commit.

> 💡You can follow [this](https://www.youtube.com/watch?v=kLKBcPonMYw&list=PL7WG7YrwYcnDb0qdPl9-KEStsL-3oaEjg&pp=iAQB) tutorial to learn about DVC in detail.