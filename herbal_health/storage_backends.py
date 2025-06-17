from storages.backends.s3boto3 import S3Boto3Storage
import os


class MediaStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = f"{bucket_name}.{os.getenv('AWS_S3_REGION_NAME')}.digitaloceanspaces.com" 