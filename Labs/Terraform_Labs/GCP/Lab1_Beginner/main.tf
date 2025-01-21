provider "google" {
    project = "<YOUR_PROJECT_ID>" # Replace with your project ID
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_compute_instance" "vm_instance" {
    name         = "terraform-vm"
    machine_type = "f1-micro"
    zone         = "us-central1-a"

    metadata = {
        startup-script = "#!/bin/bash\necho Hello, Terraform! > /tmp/terraform.log"
    }

    tags = [ "terraform-vm-tag" ]

    labels = {
        environment = "dev"
    }

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = "default"
    }
}

resource "google_storage_bucket" "terraform-lab-bucket" {
    name          = "terraform-lab-bucket-unique-12345"
    location      = "us-central1"
    force_destroy = true
}