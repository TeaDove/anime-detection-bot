from pydantic import BaseSettings


class AppSettings(BaseSettings):
    bot_token: str

    class Config:
        env_file = ".env"
        env_prefix = "service_"


app_settings = AppSettings()
