#########################################
#  IAM USER + ACCESS KEYS
#########################################
provider "aws" {
  region = var.region
}

resource "aws_iam_user" "api_user" {
  name = "api-user"
}

resource "aws_iam_access_key" "api_user_key" {
  user = aws_iam_user.api_user.name
}

#########################################
#  S3 BUCKET
#########################################

resource "aws_s3_bucket" "documents" {
  bucket = var.bucket_name

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
  }
}

# Proper versioning resource (new style)
resource "aws_s3_bucket_versioning" "documents_versioning" {
  bucket = aws_s3_bucket.documents.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Proper server-side block
resource "aws_s3_bucket_public_access_block" "block" {
  bucket                  = aws_s3_bucket.documents.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

#########################################
#  S3 BUCKET POLICY
#########################################

data "aws_iam_policy_document" "s3_policy_doc" {
  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.documents.arn,
      "${aws_s3_bucket.documents.arn}/*"
    ]
  }
}

resource "aws_iam_user_policy" "api_user_policy" {
  name   = "api-user-s3-policy"
  user   = aws_iam_user.api_user.name
  policy = data.aws_iam_policy_document.s3_policy_doc.json
}

#########################################
#  DEFAULT VPC + SUBNETS (AWS PROVIDER v5)
#########################################

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

#########################################
#  SECURITY GROUP
#########################################

resource "aws_security_group" "app_sg" {
  name        = "doc-app-sg"
  description = "Allow SSH + API access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#########################################
#  EC2 INSTANCE
#########################################

resource "aws_instance" "app_ec2" {
  instance_type               = var.instance_type
  ami                         = var.ami
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  key_name                    = aws_key_pair.dev_keypair.key_name
  associate_public_ip_address = true

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "document-app-ec2"
  }
}

#########################################
#  ECR REPOSITORY
#########################################

resource "aws_ecr_repository" "api_repo" {
  name                 = "myapi"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_lifecycle_policy" "api_repo_policy" {
  repository = aws_ecr_repository.api_repo.name

  policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Expire untagged images",
      "selection": {
        "tagStatus": "untagged",
        "countType": "imageCountMoreThan",
        "countNumber": 10
      },
      "action": { "type": "expire" }
    }
  ]
}
EOF
}



#########################################
#  OUTPUTS
#########################################

output "ec2_public_ip" {
  value = aws_instance.app_ec2.public_ip
}

output "bucket_name" {
  value = aws_s3_bucket.documents.bucket
}

output "ecr_repo_url" {
  value = aws_ecr_repository.api_repo.repository_url
}
