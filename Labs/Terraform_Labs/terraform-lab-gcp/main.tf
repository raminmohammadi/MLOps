provider "google" {
  project = "poc-lab-478221"
  region  = "us-central1"
  zone    = "us-central1-a"
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-vm"
  machine_type = "f1-micro"
  zone         = "us-central1-a"

  tags = ["ssh-allowed"]

  labels = {
    environment = "lab"
    owner       = "yashi"
  }

  metadata_startup_script = <<-EOF
    #!/bin/bash
    echo "Hello from Terraform" > /hello.txt
  EOF

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"

    access_config {
      # required to get external IP
    }
  }
}

resource "google_compute_firewall" "ssh" {
  name    = "allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh-allowed"]
}

resource "google_storage_bucket" "terraform-lab-bucket" {
  name          = "terraform-lab-bucket-unique-name-12345"
  location      = "us-central1"
  force_destroy = true

  labels = {
    environment = "lab"
    owner       = "yashi"
  }
}

output "vm_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}

output "bucket_name" {
  value = google_storage_bucket.terraform-lab-bucket.name
}