variable "region" {
  default = "us-east-1"
}

variable "environment" {
  default = "dev"
}

variable "bucket_name" {
    default = "my-unique-bucket-markjvaz-123"
}

variable "ami" {
  default = "ami-0c101f26f147fa7fd" # Amazon Linux 2023 ARM64 (valid)
}

variable "instance_type" {
  default = "t3.micro"  # ARM Free Tier
}