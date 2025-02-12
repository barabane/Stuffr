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

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
