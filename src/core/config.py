"""Settings."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """Pydantic validated settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_title: str = "WhatsApp bot"

    db_name: str
    db_username: str
    db_password: SecretStr
    db_host: str
    db_port: int

    twilio_account_sid: str
    twilio_auth_token: str
    whatsapp_sender: str

    @property
    def postgres_connection_url(self) -> URL:
        """Return URL for connections establishing to postgres."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_username,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


settings = Settings()
