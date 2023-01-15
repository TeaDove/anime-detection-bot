import boto3

from shared.settings import app_settings


class S3Supplier:
    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=app_settings.aws_access_key_id,
            aws_secret_access_key=app_settings.aws_secret_access_key,
        )
        self._s3_client = session.client(service_name="s3", endpoint_url=app_settings.endpoint)

    def safe_weights_file(self) -> str:
        try:
            open(app_settings.weights_key_local_file, "rb")
        except FileNotFoundError:
            get_object_response = self._s3_client.get_object(
                Bucket=app_settings.bucket_name, Key=app_settings.weights_key
            )
            with open(app_settings.weights_key_local_file, "wb") as f:
                f.write(get_object_response["Body"].read())
        return app_settings.weights_key_local_file
