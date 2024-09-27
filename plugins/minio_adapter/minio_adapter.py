from datetime import timedelta
import hashlib
import os
from uuid import uuid4
from minio import Minio
from plugins.base import AbstractStorageServiceAdapter


class MinioAdapter(AbstractStorageServiceAdapter):
    def __init__(self, config=None) -> None:
        if config is None:
            raise ValueError("Configuration for MinioAdapter must be provided.")

        self.bucket_name = config['bucket_name']
        self.public_bucket_name = "public-" + self.bucket_name
        self.client = Minio(**config['config'])
        self.config = config

        if not self.client.bucket_exists(self.bucket_name):
            print(f'Creating bucket: {self.bucket_name}...')
            self.client.make_bucket(self.bucket_name)

    def get(self, file_name, is_public=False) -> str:
        if is_public:
            protocol = "https" if self.config['config'].get('secure', False) else "http"
            return f"{protocol}://{self.config['config']['endpoint']}/{self.public_bucket_name}/{file_name}"
        return self.client.presigned_get_object(
            bucket_name=self.bucket_name, object_name=file_name
        )

    def _calculate_hash(self, file) -> str:
        hash_object = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)
        return hash_object.hexdigest()

    def deep_check_for_duplicates(self, file) -> dict:
        file_hash = self._calculate_hash(file)
        objects = self.client.list_objects(bucket_name=self.bucket_name)
        for obj in objects:
            obj_data = self.client.get_object(
                bucket_name=self.bucket_name, object_name=obj.object_name
            )
            obj_hash = self._calculate_hash(obj_data)
            if obj_hash == file_hash:
                return {"name": obj.object_name}
        return None

    def save(self, file, deep_check=False, is_public=False) -> dict:
        name = str(uuid4()) + "." + file.name.split(".")[-1]
        if deep_check:
            duplicate = self.deep_check_for_duplicates(file)
            if duplicate:
                return duplicate
        try:
            size = file.size
        except AttributeError:
            size = os.path.getsize(file.name)
        bucket_name = self.bucket_name if not is_public else self.public_bucket_name
        self.client.put_object(
            bucket_name=bucket_name, object_name=name, data=file, length=size
        )
        return {"name": name}

    def delete(self, file_name) -> dict:
        self.client.remove_object(bucket_name=self.bucket_name, object_name=file_name)
        return {"status": "deleted", "name": file_name}

    def get_temp_upload_url(self, file_name, expiry=timedelta(hours=1), is_public=False) -> str:
        if is_public:
            return self.client.presigned_put_object(self.public_bucket_name, file_name, expires=expiry)
        return self.client.presigned_put_object(self.public_bucket_name, file_name, expires=expiry)
