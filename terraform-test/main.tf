provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "terraform-test-bucket-markjvaz-123456789"
  force_destroy = true

  tags = {
    Name = "Terraform Test"
  }
}
