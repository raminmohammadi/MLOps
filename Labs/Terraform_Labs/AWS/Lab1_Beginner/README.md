# Terraform Beginner Lab

## Objective
Learn the fundamentals of Terraform by creating, managing, and destroying a simple AWS infrastructure resource. By the end of this lab, students will:

- Understand the purpose of Terraform.
- Install and configure Terraform.
- Write and apply a basic Terraform configuration.
- Use Terraform commands to manage infrastructure.
- You can follow along step by step, or you can just run the commands using the code in `main.tf`.
- The video for the lab can be found [here](). # need to add a video link

## Prerequisites
- An AWS account.
- AWS access keys set up.
- Terraform installed on your local machine (https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

### Create AWS access key

1. Open the AWS console.
2. Navigate to the **Security Credentials** page under **IAM**.
3. Click **Create access key**.
4. Enter a name for the key (for example, **mykey**).
5. Click **Create**.
6. Copy the **Access key ID** and **Secret access key** to your clipboard. This is the only time you will be able to see the secret key. Copy the key to a secure location.

### Set the environment variables

1. Open a terminal or command prompt.
2. Run the following command to set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables:

    ```bash
    export AWS_ACCESS_KEY_ID=<your-access-key-id>
    export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
    ```

    Replace `<your-access-key-id>` and `<your-secret-access-key>` with your actual access key ID and secret access key.

    This will only work for the current session. If you want to set these variables permanently, you will have to set the environment variables in your system's environment variables, based on the OS you are using.

## Part 1: Setting up Terraform

1. Verify Terraform is installed on your local machine.

    ```bash
    terraform --version
    ```

2. Create a directory for your Terraform files.

    ```bash
    mkdir terraform-lab-aws
    cd terraform-lab-aws
    ```

3. Create a file named `main.tf` and add the following code:

    ```h
    provider "aws" {
        region = "us-east-1"
    }

    resource "aws_instance" "myec2" {
        ami = "ami-0e2c8caa4b6378d8c"
        instance_type = "t2.micro"
    }
    ```

    The `provider` block configures the AWS provider to use the `us-east-1` region. The `resource` block creates an EC2 instance with the specified AMI and instance type. You can create any other ec2 instance you want by modifying the `ami` and `instance_type` values.

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
    The `plan` command will show the changes that Terraform will make to your infrastructure.

2. **Apply the infrastructure**: Apply the changes to your infrastructure.

    ```bash
    terraform apply
    ```

    The `apply` command will apply the changes that Terraform made to your infrastructure. Confirm by typing `yes` at the prompt. You can also use the `terraform apply -auto-approve` command to automatically approve the changes.

3. **View the changes in the AWS console**: Check the AWS console to see the changes that Terraform made to your infrastructure.

    - Open the AWS console.
    - Navigate to the **EC2** page.
    - Find the instance that Terraform created.
    - Click on the instance to view its details.

## Part 3: Modifying Resources

You can modify any resource in the configuration file and apply the changes using the `terraform apply` command.

1. **Modify the EC2 instance**: Add the Name tag to the EC2 instance.

    ```h
    resource "aws_instance" "myec2" {
        ami = "ami-0e2c8caa4b6378d8c"
        instance_type = "t2.micro"
        tags = {
            Name = "MyEC2Instance"
        }
    }
    ```

2. **Apply the changes**: Apply the changes to your infrastructure.

    ```bash
    terraform apply
    ```

3. **View the changes in the AWS console**: Check the EC2 instance in the AWS console and confirm that the Name tag was added.

## Part 4: Adding more resources

Let's explore adding another resource to the configuration file.

1. **Add a VPC and subnet**: Add a VPC and subnet to the configuration file.

    ```h
    resource "aws_vpc" "myvpc" {
        cidr_block = "10.0.0.0/16"
        tags = {
            Name = "myvpc"
        }
    }

    resource "aws_subnet" "mysubnet1" {
        vpc_id = aws_vpc.myvpc.id
        cidr_block = "10.0.1.0/24"
        tags = {
            Name = "mysubnet1"
        }
    }
    ```
    The `aws_vpc` resource creates a VPC with the specified CIDR block. The `aws_subnet` resource creates a subnet within the VPC with the specified CIDR block. The `vpc_id` attribute is used to specify the VPC in which the subnet should be created.

2. **Apply the changes**: Apply the changes to your infrastructure.

    ```bash
    terraform apply
    ```

3. **View the changes in the AWS console**: Check the VPC and subnet in the AWS console and confirm that they were created.

## Part 5: Destroying Resources

You can destroy any resource in the configuration file and apply the changes using the `terraform destroy` command.

1. **Use the `terraform destroy` command**: Destroy the resources that Terraform created.

    ```bash
    terraform destroy
    ```

    The `destroy` command will destroy the resources that Terraform created. Confirm by typing `yes` at the prompt.

2. **View the changes in the AWS console**: Check the resources in the AWS console and confirm that they were destroyed.

3. **Destroy using the config file**: Another way to destroy any resource is to remove it from the configuration file, and then run `terraform apply`. Terraform will detect the changes and destroy the resource. You can view the changes that are going to be applied using `terraform plan`, before applying the changes.

## Part 6: Understanding different Terraform files

1. **State file**:
    Terraform uses state files to keep track of the resources it manages. The state file is created when you run `terraform apply` and contains information about the resources Terraform manages.

    The state file `terraform.tfstate` is a JSON file that contains the current state of the resources Terraform manages.

    State files are critical for tracking changes; ensure they are securely stored. No manual changes should ever be made to the state file.

2. **Terraform directory**:
    When you execute `terraform init`, a `.terraform` directory is created in the current working directory, and all the required plugins and provider files are downloaded in this directory.