from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings, Field

# Environment
from app.schemas import GenericSchema

# Application
class Application(BaseSettings):
    application_name: str = Field(env="APPLICATION_NAME")
    env_mode: GenericSchema.EnvironmentMode = Field(
        env="APPLICATION_ENVIRONMENT", default=GenericSchema.EnvironmentMode.DEV
    )
    log_level: GenericSchema.LogLevel = Field(
        env="APPLICATION_LOG_LEVEL", default=GenericSchema.LogLevel.DEUBG
    )


# JWT
class JWT(BaseSettings):
    secret_key: str = Field(env="JWT_SECRET_KEY")
    algorithm: str = Field(env="JWT_ALGORITHM")
    expire_min: int = Field(120, env="JWT_EXPIRE_TIME_MINUTE")


# Sentry
class SentryConfiguration(BaseSettings):
    dns: Optional[str] = Field(env="SENTRY_DNS")
    trace_sample_rates: Optional[float] = Field(
        env="SENTRY_TRACE_SAMPLE_RATE", default=1.0
    )


class Settings(BaseSettings):
    # Application
    app: Application = Application()

    # JWT
    jwt: JWT = JWT()

    # Sentry Monitor
    sentry: SentryConfiguration = SentryConfiguration()


@lru_cache(maxsize=50)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
