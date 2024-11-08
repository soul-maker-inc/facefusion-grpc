from minio import Minio
import tempfile
import uuid
import os
import hashlib
from simple_file_checksum import get_checksum
from datetime import timedelta


MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT') or "127.0.0.1:9000"
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY') or "nwmqlO3PeJvSA4FjY2kI"
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY') or "3F4872HE27Pjms7N0hATQfCTbnI6GBkZv5ExlfjU"
MINIO_BUCKET = os.environ.get('MINIO_BUCKET') or "ark"
MINIO_ENABLE_SSL = os.environ.get('MINIO_ENABLE_SSL') or False

def download_minio(objecturl):
    objecturl = objecturl.removeprefix("oss://")
    tmpPath = tempfile.gettempdir()
    filename = str(uuid.uuid4()) + os.path.splitext(objecturl)[1]
    client = Minio(MINIO_ENDPOINT, MINIO_ACCESS_KEY,
                   MINIO_SECRET_KEY, None, MINIO_ENABLE_SSL)
    client.fget_object(bucket_name=MINIO_BUCKET,
                       object_name=objecturl, file_path=tmpPath + "/" + filename)
    return tmpPath + "/" + filename


def upload_to_minio(localfile, osspath):
    filename = osspath + get_checksum(localfile, algorithm="MD5") + \
        os.path.splitext(localfile)[1]
    client = Minio(MINIO_ENDPOINT, MINIO_ACCESS_KEY,
                   MINIO_SECRET_KEY, None, MINIO_ENABLE_SSL)
    client.fput_object(MINIO_BUCKET, filename.removeprefix('/'), localfile)
    return filename
