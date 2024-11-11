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

    class Config:
        env_file = ".env"
        

application_settings = ApplicationSettings()