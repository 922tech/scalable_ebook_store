import os
import unittest
import requests
from io import BytesIO
from .minio_adapter import MinioAdapter


CLOUD_STORAGE_CLIENT_CONFIG = {
    'backend': 'plugins.minio_adapter.minio_adapter.MinioAdapter',
    'bucket_name': os.getenv('MINIO_PUBLIC_BUCKET_NAME', 'public'),
    'config': {
        'endpoint': os.getenv('MINIO_ENDPOINT_URL', 'localhost:9000'),
        'access_key': os.getenv('MINIO_ACCESS_KEY', 'BUCKET_ACCESS_KEY'),
        'secret_key': os.getenv('MINIO_SECRET_KEY', 'BUCKET_SECRET_KEY'),
        'secure': bool(os.getenv('BUCKET_SECURE', 0)),
    }
}


class TestMinioAdapterIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.adapter = MinioAdapter(CLOUD_STORAGE_CLIENT_CONFIG)
        cls.bucket_name = CLOUD_STORAGE_CLIENT_CONFIG['bucket_name']

    def setUp(self):
        self.test_file_content = b"Hello, MinIO!"
        self.test_file = BytesIO(self.test_file_content)
        self.test_file.name = 'testfile.txt'
        self.test_file.size = len(self.test_file_content)

    def test_generate_presigned_url(self):
        # Generate a presigned URL for uploading
        file_name = 'upload_testfile.txt'
        presigned_url = self.adapter.get_temp_upload_url(file_name)

        # Use the presigned URL to upload the file
        response = requests.put(presigned_url, data=self.test_file_content)

        # Check if the upload was successful
        self.assertEqual(response.status_code, 200)

        # Verify the file is accessible
        download_url = self.adapter.get(file_name, is_public=False)
        response = requests.get(download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.test_file_content)
        print('PASSEDS!')

    def tearDown(self):
        # Clean up the test file from the bucket
        try:
            self.adapter.delete('upload_testfile.txt')
        except Exception as e:
            print(f"Error deleting file: {e}")


if __name__ == '__main__':
    unittest.main()
