provider "aws" {
    region = "us-east-1"
}

# resource "<provider>_<resource_type>" "<resource_name>" {
#     <attribute> = "<value>"
# }

resource "aws_instance" "myec2" {
    ami = "ami-0e2c8caa4b6378d8c"
    instance_type = "t2.micro"
    tags = {
        Name = "myec2"
    }
}

resource "aws_subnet" "mysubnet1" {
    vpc_id = aws_vpc.myvpc.id
    cidr_block = "10.0.1.0/24"
    tags = {
        Name = "mysubnet1"
    }
}

resource "aws_vpc" "myvpc" {
    cidr_block = "10.0.0.0/16"
    tags = {
        Name = "myvpc"
    }
}