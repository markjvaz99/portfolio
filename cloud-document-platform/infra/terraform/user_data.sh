#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
systemctl start docker
usermod -aG docker ec2-user

# Install docker-compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone repo
cd /home/ec2-user
git clone https://github.com/markjvaz99/portfolio.git services/api/app
cd services/api/app

# Create env file
cat <<EOF > .env
AWS_ACCESS_KEY_ID=${api_user_access_key_id}
AWS_SECRET_ACCESS_KEY=${api_user_secret_key}
AWS_REGION=us-east-1
S3_BUCKET=${bucket_name}
DATABASE_URL=postgresql+asyncpg://app:password@postgres:5432/appdb
REDIS_URL=redis://redis:6379/0
EOF

docker-compose up -d
