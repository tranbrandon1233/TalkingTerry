from dotenv import load_dotenv
import os
from google.cloud import storage
load_dotenv()
GCP_ACCESS_TOKEN = os.getenv("GCP_ACCESS_TOKEN")
GCP_REFRESH_TOKEN = os.getenv("GCP_REFRESH_TOKEN")
GCP_REFRESH_TOKEN = os.getenv("GCP_REFRESH_TOKEN")
API_HOST_UPLOAD = 'https://storage.googleapis.com/upload/storage/v1/b/{0}/o'.format("terrys-memories")
API_HOST_DOWNLOAD = 'https://storage.googleapis.com/upload/storage/v1/b/{0}/o'.format("terrys-memories")


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(project='reflected-alpha-232601')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    return "Operation completed successfully."


def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client(project='reflected-alpha-232601')

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    contents = blob.download_as_string()

    return contents