import os
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    jwt_secret_key: str
    jwt_algo: str = "HS256"
    jwt_expiration_time: int

    profile_picture_filename: str
    profile_picture_extension: str
    profile_pictures_path: str
    profile_pictures_mount_point: str

    smtp_server_host: str
    smtp_server_port: str
    smtp_server_login: str
    smtp_server_password: str

    email_confirmation_url_expiration_time: int

    frontend_domain: str
    hostname: str

    class Config:
        env_file = ".env"


application_settings = ApplicationSettings()
application_settings.profile_pictures_path = os.path.expanduser(
    application_settings.profile_pictures_path
)
