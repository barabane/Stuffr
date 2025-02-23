from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_NAME: str
    POSTGRES_PASS: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POSTGRES_URL: str

    TOKEN_SECRET: str
    TOKEN_ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION: int
    REFRESH_TOKEN_EXPIRATION: int
    RESET_TOKEN_EXPIRATION: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    CELERY_BROKER: str
    CELERY_BACKEND: str

    RESET_PASSWORD_URL: str

    REDIS_URL: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
