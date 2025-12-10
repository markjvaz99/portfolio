output "api_user_access_key" {
  value = aws_iam_access_key.api_user_key.id
  description = "Access key ID for the API user"
}

output "api_user_secret_key" {
  value = aws_iam_access_key.api_user_key.secret
  description = "Secret key for the API user"
  sensitive   = true
}
