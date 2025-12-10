# services/api/app/utils/s3.py
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)

def _upload(fileobj, bucket, key):
    # boto3 is blocking; called in threadpool when used in async code
    fileobj.seek(0)
    s3.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=key)

async def upload_fileobj_to_s3(fileobj, key: str, bucket: str = None):
    bucket = bucket or settings.s3_bucket
    loop = asyncio.get_event_loop()
    # ensure fileobj is a file-like object (BytesIO or similar)
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, _upload, fileobj, bucket, key)
    return {"bucket": bucket, "key": key}

def download_to_bytes(bucket: str, key: str) -> bytes:
    out = io.BytesIO()
    s3.download_fileobj(Bucket=bucket, Key=key, Fileobj=out)
    out.seek(0)
    return out.read()
