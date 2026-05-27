from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IA de Analítica de BD"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    sessions_db_url: str = "sqlite:///./sessions.db"
    analytics_db_url: str = "postgresql://user:pass@host:5432/db"
    openrouter_api_key: str = ""
    ai_model: str = "poolside/laguna-m.1:free"
    allowed_origins: str = "http://localhost:5173"
    log_level: str = "INFO"
    
    # Auth
    secret_key: str = "dev_secret_key_change_me_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours for MVP convenience

    @field_validator("analytics_db_url")
    @classmethod
    def validate_analytics_url(cls, v: str) -> str:
        if v and not v.startswith("postgresql") and not v.startswith("sqlite"):
            raise ValueError("ANALYTICS_DB_URL must be a PostgreSQL or SQLite connection string")
        return v

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: str) -> str:
        return v

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
