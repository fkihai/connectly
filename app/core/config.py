from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_HOST: str

    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_EMAIL: str

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
