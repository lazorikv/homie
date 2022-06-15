from os.path import isfile, join
import boto3
from os import listdir
from backend import settings
from botocore.exceptions import ClientError


def upload_file(path, bucket, object_name=None):
    """
    Upload files to an S3 bucket

    :param bucket: Bucket to upload to
    :param path: Path of the folder with files to upload
    :param object_name: S3 object name. If not specified, then filename is used
    :return: True if file was uploaded, else False
    """

    # S3 bucket connection
    s3_client = boto3.client("s3",
                             aws_access_key_id=settings.USER_ACCESS_ID,
                             aws_secret_access_key=settings.USER_ACCESS_KEY)

    # List files from a folder
    try:
        files = [f for f in listdir(path) if isfile(f)]
    except NotADirectoryError:
        files = [path]

    try:
        # Upload the image
        for file in files:
            s3_client.upload_file(file, bucket, object_name)

    except ClientError:
        return False

    return True
