
# Kubeflow Deployment on Google Cloud



---

## 1. Set Up a Google Cloud Project
- Create or select a GCP project on the [Google Cloud Console](https://console.cloud.google.com).
- Ensure you have the **Owner role** for the project in Cloud IAM, as the deployment creates service accounts with necessary permissions.
- Enable the necessary APIs by running the following command:
```bash
gcloud services enable serviceusage.googleapis.com \
    compute.googleapis.com \
    container.googleapis.com \
    iam.googleapis.com \
    servicemanagement.googleapis.com \
    cloudresourcemanager.googleapis.com \
    ml.googleapis.com \
    iap.googleapis.com \
    sqladmin.googleapis.com \
    meshconfig.googleapis.com \
    krmapihosting.googleapis.com \
    servicecontrol.googleapis.com \
    endpoints.googleapis.com \
    cloudbuild.googleapis.com
```
- Next, initialize your project to prepare it for Anthos Service Mesh installation. This will configure the necessary infrastructure for the service mesh.
```bash
PROJECT_ID=<YOUR_PROJECT_ID>
````
- Create a temporary cluster
```bash
gcloud beta container clusters create tmp-cluster \
  --release-channel regular \
  --workload-pool=${PROJECT_ID}.svc.id.goog
 ```
```bash
curl --request POST \
  --header "Authorization: Bearer $(gcloud auth print-access-token)" \
  --data '' \
  https://meshconfig.googleapis.com/v1alpha1/projects/${PROJECT_ID}:initialize

```

## 2. Set Up OAuth Client
- Go to the **Credentials** section in the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
- Create an **OAuth 2.0 Client ID** and configure the consent screen for your users.
- Save the OAuth **Client ID** and **Client Secret**, as they will be used later in the deployment process.
- On the Create credentials screen, find your newly created OAuth credential and click the pencil icon to edit it
- In the Authorized redirect URIs box, enter the following:

```bash
https://iap.googleapis.com/v1/oauth/clientIds/<CLIENT_ID>:handleRedirect
```
- <CLIENT_ID> is the OAuth client ID that you copied from the dialog box in step four. It looks like XXX.apps.googleusercontent.com.
---

## 3. Deploy the Management Cluster

- Install the required google components:
```bash
sudo apt-get install kubectl google-cloud-cli-kpt google-cloud-cli-anthoscli google-cloud-cli
```
- Install kustomise:
```bash
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash

sudo mv kustomize /usr/local/bin/
```

- Install kpt:
```bash
wget https://github.com/GoogleContainerTools/kpt/releases/download/v1.0.0-beta.6/kpt_linux_amd64-1.0.0-beta.6.tar.gz

tar -zxvf kpt_linux_amd64-1.0.0-beta.6.tar.gz

sudo mv kpt /usr/local/bin/
```

- Update the components:
```bash
gcloud components update
```
- Clone the Kubeflow distribution repository:
```bash
git clone https://github.com/googlecloudplatform/kubeflow-distribution.git
cd kubeflow-distribution
git checkout master
```
- Go to kubeflow-distribution/management directory for Management cluster configurations.
```bash
cd management
```
- Fill in environment variables in kubeflow-distribution/management/env.sh as followed:
- Ensure that a different location from 'us-central1' is chosen, and it should also not be the same location used to create the 'tmp-cluster'.
```commandline
MGMT_PROJECT=<the project where you deploy your management cluster>

MGMT_NAME=<name of your management cluster>

LOCATION=<location of your management cluster to us-eastX>
```
- Set up environment variables by editing and running:
```bash
source kubeflow/env.sh
```
- Use kpt to set values for the name, project, and location of your management cluster
```bash
bash ./kpt-set.sh
```
- Install kubectl:
```bash
gcloud components install kubectl
```

- Set the Google Cloud project where you want to host Config Controller:
```bash
gcloud config set project <PROJECT_ID>
```
- Enable the APIs that you require:

```bash
gcloud services enable krmapihosting.googleapis.com \
    anthos.googleapis.com  \
    cloudresourcemanager.googleapis.com \
    serviceusage.googleapis.com
```
- Deploy the management cluster by applying cluster resources:
```bash
make create-cluster
```

- Create a kubectl context for the management cluster, it will be named ${MGMT_NAME}:
```bash
make create-context
```

- Grant permission to Config Controller service account:
```bash
make grant-owner-permission 
```
---

## 4. Deploy the Kubeflow Cluster

- Run the following command to pull upstream manifests from kubeflow/manifests repository.
```bash
cd kubeflow

bash ./pull-upstream.sh
```

- Review and fill all the environment variables in kubeflow-distribution/kubeflow/env.sh
- After defining these environment variables, run:
```bash
source env.sh
```
- Set environment variables with OAuth Client ID and Secret for IAP:
```bash
export CLIENT_ID=<Your CLIENT_ID>
export CLIENT_SECRET=<Your CLIENT_SECRET>
```
-Run the following commands to configure kpt setter for your Kubeflow cluster:
```bash
bash ./kpt-set.sh
```
-Set the Management environment variable:
```bash
MGMT_PROJECT=<the project where you deploy your management cluster>
MGMT_NAME=<the kubectl context name for management cluster>
```
- Apply ConfigConnectorContext for ${KF_PROJECT} in management cluster:
```bash
make apply-kcc
```
- Make sure you are using KF_PROJECT in the gcloud CLI tool:
```bash
gcloud config set project ${KF_PROJECT}
```

- To deploy the Kubeflow cluster, use:
```bash
make apply
```
- If any errors occur due to race conditions or missing API groups, rerun the `make apply` command.

---

## 5. Access the Kubeflow Dashboard
- Once deployed, you can access the Kubeflow UI by assigning yourself the **IAP-secured Web App User** role and navigating to the provided URL in the deployment logs.
```bash
gcloud projects add-iam-policy-binding "${KF_PROJECT}" --member=user:<EMAIL> --role=roles/iap.httpsResourceAccessor
```

- Enter the following URI into your browser address bar. It can take 20 minutes for the URI to become available: 
```commandline
https://${KF_NAME}.endpoints.${KF_PROJECT}.cloud.goog/
```
- You can run the following command to get the URI for your deployment:
```bash
kubectl -n istio-system get ingress
```
For more details on troubleshooting and customization options, refer to the [Kubeflow on GCP documentation](https://googlecloudplatform.github.io/kubeflow-gke-docs/docs/deploy/).
