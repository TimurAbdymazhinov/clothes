import boto3
from decouple import config


class S3Service:
    def __init__(self):
        self.key = config("AWS_ACCESS_KEY")
        self.secret = config("AWS_SECRET_KEY")
        self.s3 = boto3.client(
            "s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret
        )
        self.bucket_name = config("AWS_BUCKET_NAME")

    def upload(self, path, key, ext):
        self.s3.upload_file(
            path, self.bucket_name, key,
            ExtraArgs={
                "ACL": "public-read",  "ContentType": f"image/{ext}",
            }
        )
        return f"https://{self.bucket_name}.s3.amazonaws.com/{key}"
