# Terraform Beginner Lab (GCP Version)

## Objective
Learn the fundamentals of Terraform by creating, managing, and destroying a simple GCP infrastructure resource. By the end of this lab, students will:

- Understand the purpose of Terraform.
- Install and configure Terraform.
- Write and apply a basic Terraform configuration.
- Use Terraform commands to manage infrastructure.
- You can follow along step by step, or you can just run the commands using the code in `main.tf`.
- The video for the lab can be found [here](). # need to add a video link

## Prerequisites
- A GCP account with billing enabled.
- Google Cloud CLI installed and configured.
- A project set up in GCP with a linked billing account.
- Terraform installed on your local machine (https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli).

### Create a Service Account and Key

1. Open the GCP Console.
2. Navigate to **IAM & Admin > Service Accounts**.
3. Click **Create Service Account**.
4. Enter a name (e.g., `terraform-service-account`).
5. Assign the `Editor` role for simplicity (or specific roles as required).
6. Click **Create and Continue**.
7. Generate and download the JSON key file.

### Set the environment variables

1. Open a terminal or command prompt.
2. Run the following command to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-key-file.json"
    ```

    Replace `/path/to/your-key-file.json` with the actual path to your key file. This will only work for the current session. If you want to set this variable permanently, you will have to set the environment variable in your system's environment variables, based on the OS you are using.

## Part 1: Setting up Terraform

1. Verify Terraform is installed on your local machine:
    ```bash
    terraform --version
    ```

2. Create a directory for your Terraform files:
    ```bash
    mkdir terraform-lab-gcp
    cd terraform-lab-gcp
    ```

3. Create a file named `main.tf` and add the following code:
    ```hcl
    provider "google" {
        project = "your-project-id" # Replace with your project ID
        region  = "us-central1"
        zone    = "us-central1-a"
    }

    resource "google_compute_instance" "vm_instance" {
        name         = "terraform-vm"
        machine_type = "f1-micro"
        zone         = "us-central1-a"

        boot_disk {
            initialize_params {
                image = "debian-cloud/debian-11"
            }
        }

        network_interface {
            network = "default"
        }
    }
    ```
    The `provider` block configures the Google Cloud provider, specifying the project, region, and zone. The `resource` block creates a VM instance with the specified configuration.

    The machine type is set to `f1-micro`, which is a free tier instance type. The `zone` is set to `us-central1-a`, which is a default zone in the `us-central1` region. 
    
    The `boot_disk` block specifies the image to use for the boot disk, and the `network_interface` block configures the network settings.

4. Initialize Terraform:
    ```bash
    terraform init
    ```
    On initialization, Terraform will download the required providers and plugins.

## Part 2: Applying the Terraform Configuration

1. **Plan the infrastructure**: Review the changes that Terraform will make to your infrastructure.
    ```bash
    terraform plan
    ```

2. **Apply the infrastructure**: Apply the changes to your infrastructure.
    ```bash
    terraform apply
    ```
    Confirm by typing `yes` at the prompt. You can also use the `terraform apply -auto-approve` command to automatically approve the changes.

3. **View the changes in the GCP Console**: Check the **Compute Engine** section to see the instance created by Terraform.

## Part 3: Modifying Resources

You can modify any resource in the configuration file and apply the changes using the `terraform apply` command.

1. **Modify the VM instance**: Add metadata to the VM instance.
    ```hcl
    resource "google_compute_instance" "vm_instance" {
        name         = "terraform-vm"
        machine_type = "f1-micro"
        zone         = "us-central1-a"

        metadata = {
            startup-script = "#!/bin/bash\necho Hello, Terraform! > /tmp/terraform.log"
        }

        boot_disk {
            initialize_params {
                image = "debian-cloud/debian-11"
            }
        }

        network_interface {
            network = "default"
            access_config {
            }
        }
    }
    ```

2. **Apply the changes**: Apply the changes to your infrastructure.
    ```bash
    terraform apply
    ```

3. **View the changes in the GCP Console**: Check the **Compute Engine** section and confirm that the metadata was added.

## Part 4: Adding More Resources

1. **Add a Cloud Storage bucket**:
    ```hcl
    resource "google_storage_bucket" "terraform-lab-bucket" {
        name          = "terraform-lab-bucket-unique-name" # must be unique
        location      = "us-central1"
        force_destroy = true
    }
    ```

2. **Apply the changes**:
    ```bash
    terraform apply
    ```

3. **View the changes in the GCP Console**: Check the **Cloud Storage** section and confirm that the bucket was created.

## Part 5: Destroying Resources

1. **Use the `terraform destroy` command**: Destroy the resources that Terraform created.
    ```bash
    terraform destroy
    ```
    Confirm by typing `yes` at the prompt.

2. **View the changes in the GCP Console**: Check the resources in the GCP Console and confirm that they were destroyed.

3. **Destroy using the config file**: Another way to destroy a resource is to remove it from the configuration file and then run `terraform apply`. Terraform will detect the changes and destroy the resource. Use `terraform plan` to preview the changes.

## Part 6: Understanding Different Terraform Files

1. **State file**:
    Terraform uses state files to keep track of the resources it manages. The state file is created when you run `terraform apply` and contains information about the resources Terraform manages.

    The state file `terraform.tfstate` is a JSON file that contains the current state of the resources Terraform manages.

    State files are critical for tracking changes; ensure they are securely stored. No manual changes should ever be made to the state file.

2. **Terraform directory**:
    When you execute `terraform init`, a `.terraform` directory is created in the current working directory, and all the required plugins and provider files are downloaded in this directory.
