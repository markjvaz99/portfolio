# Generate an SSH key pair locally
resource "tls_private_key" "dev_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Upload the public key to AWS as an EC2 Key Pair
resource "aws_key_pair" "dev_keypair" {
  key_name   = "dev-key"
  public_key = tls_private_key.dev_key.public_key_openssh
}

# Save the private key locally so you can SSH
resource "local_file" "private_key" {
  content              = tls_private_key.dev_key.private_key_pem
  filename             = "${path.module}/dev-key.pem"
  file_permission      = "0400"
}
