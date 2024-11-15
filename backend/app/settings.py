from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    jwt_secret_key: str
    jwt_algo: str = "HS256"
    jwt_expiration_time: int = 60
    profile_picture_filename: str
    profile_picture_extension: str
    profile_picture_path: str
    
    class Config:
        env_file = ".env"


application_settings = ApplicationSettings()
