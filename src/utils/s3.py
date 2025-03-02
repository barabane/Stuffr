from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from fastapi import UploadFile

from src.config import settings


class S3_Bucket:
    def __init__(
        self,
        access_key: str = settings.S3_ACCESS,
        secret_key: str = settings.S3_SECRET,
        endpoint_url: str = settings.S3_URL,
        bucket_name: str = settings.S3_BUCKET,
        region: str = settings.S3_REGION,
    ):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
            'region_name': region,
        }
        self.bucket_name = bucket_name
        self.async_session = get_session()

    @asynccontextmanager
    async def get_async_client(self):
        async with self.async_session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(self, file: UploadFile, name: str, folder: str = None) -> str:
        file_name = f'{folder}/{name}' if folder else name

        async with self.get_async_client() as client:
            await client.put_object(
                Bucket=self.bucket_name, Key=file_name, Body=file.file
            )
            return self.get_file_link(file_name)

    async def delete_file(self, object_name: str) -> None:
        async with self.get_async_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)

    def get_file_link(self, file_name: str) -> str:
        return f'{self.config["endpoint_url"]}{self.bucket_name}/{file_name}'


s3_bucket = S3_Bucket()
