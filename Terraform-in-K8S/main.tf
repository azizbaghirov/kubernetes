terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  access_key = <ACCESS KEY IN DOUBLE QUOUTES>
  secret_key = <SECRET KEY IN DOUBLE QUOUTES>
  region = "us-east-2"
}

resource "aws_instance" "testinstance" {
  ami           = "ami-0c7c4e3c6b4941f0f"
  instance_type = "t2.micro"

  tags = {
    Name = "testinstance"
  }
}
