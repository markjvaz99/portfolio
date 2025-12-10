# Create IAM user for your API
resource "aws_iam_user" "api_user" {
  name = "api-user"
}

# Create access keys for the user
resource "aws_iam_access_key" "api_user_key" {
  user = aws_iam_user.api_user.name
}

resource "aws_s3_bucket" "documents" {
  bucket = var.bucket_name  # must be globally unique
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
  }
}

# Optional: block public access
resource "aws_s3_bucket_public_access_block" "block" {
  bucket                  = aws_s3_bucket.documents.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# Create IAM policy allowing access to your bucket
data "aws_iam_policy_document" "s3_policy_doc" {
  statement {
    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket"
    ]

    resources = [
      aws_s3_bucket.documents.arn,          # bucket itself
      "${aws_s3_bucket.documents.arn}/*"    # all objects in bucket
    ]
  }
}

# Attach policy to IAM user
resource "aws_iam_user_policy" "api_user_policy" {
  name   = "api-user-s3-policy"
  user   = aws_iam_user.api_user.name
  policy = data.aws_iam_policy_document.s3_policy_doc.json
}
