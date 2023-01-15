from pydantic import BaseSettings


class AppSettings(BaseSettings):
    endpoint: str = "https://storage.yandexcloud.net"
    bucket_name: str = "stable-anime-detection-bot-backend-wiegth-bucket"
    weights_key: str = "model.pth"
    weights_key_local_file: str = "model.pth"

    aws_access_key_id: str
    aws_secret_access_key: str

    uvicorn_workers: int = 1

    class Config:
        env_file = ".env"
        env_prefix = "service_"


app_settings = AppSettings()
