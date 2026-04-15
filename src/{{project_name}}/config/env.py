from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, PostgresDsn


class _Settings(BaseSettings):
    app_name: str
    app_env: Literal['dev', 'test', 'prod', 'homolog']
    db_name: str
    db_server: str
    db_user: str
    db_pass: str
    db_port: int
    debug: bool
    secret: str
    jwt_algorithm: str
    jwt_issuer: str
    jwt_audience: str
    auth_service_url: str
    token_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @computed_field
    @property
    def database_url(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.db_user,
                password=self.db_pass,
                host=self.db_server,
                port=self.db_port,
                path=f'/{self.db_name}'
            )
        )
    
    @computed_field
    @property
    def token_endpoint(self) -> str:
        return f"{self.auth_service_url}{self.token_url}"


class TestSettings(_Settings):

    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> _Settings:
    return _Settings()


Settings = Annotated[_Settings, Depends(get_settings)]