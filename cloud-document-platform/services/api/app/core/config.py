# services/api/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "local"
    database_url: str
    redis_url: str = "redis://redis:6379/0"
    s3_bucket: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

