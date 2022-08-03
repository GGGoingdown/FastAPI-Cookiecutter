from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings, Field
from kombu import Queue

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
    log_path: str = Field(env="APPLICATION_LOG_PATH", default="/var/log/application")


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


# Redis
class RedisConfiguration(BaseSettings):
    host: str = Field(env="REDIS_HOST")
    port: str = Field(env="REDIS_PORT")
    username: str = Field(env="REDIS_USERNAME")
    password: str = Field(env="REDIS_PASSWORD")
    backend_db: int = Field(0, env="REDIS_BACKEND_DB")
    result_db: int = Field(1, env="REDIS_RESULT_DB")


# Postgres
class PostgresConfiguration(BaseSettings):
    host: str = Field(env="POSTGRES_HOST")
    port: str = Field(env="POSTGRES_PORT")
    username: str = Field(env="POSTGRES_USERNAME")
    password: str = Field(env="POSTGRES_PASSWORD")
    db: str = Field(env="POSTGRES_DB")


# RabbitMQ
class RabbitMQConfiguration(BaseSettings):
    host: str = Field(env="RABBITMQ_HOST")
    port: str = Field(env="RABBITMQ_PORT")
    username: str = Field(env="RABBITMQ_USERNAME")
    password: str = Field(env="RABBITMQ_PASSWORD")


class Settings(BaseSettings):
    # Application
    app: Application = Application()

    # JWT
    jwt: JWT = JWT()

    # Sentry Monitor
    sentry: SentryConfiguration = SentryConfiguration()

    # RDBMS
    pg: PostgresConfiguration = PostgresConfiguration()

    # Redis
    redis: RedisConfiguration = RedisConfiguration()

    # RabbitMQ
    rabbitmq: RabbitMQConfiguration = RabbitMQConfiguration()


@lru_cache(maxsize=50)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


# Celery Configuration
class CeleryConfiguration:
    broker_url = f"amqp://{settings.rabbitmq.username}:{settings.rabbitmq.password}@{settings.rabbitmq.host}:{settings.rabbitmq.port}//"

    result_backend = f"redis://{settings.redis.username}:{settings.redis.password}@{settings.redis.host}:{settings.redis.port}/{settings.redis.result_db}"

    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]

    task_queues = (Queue("high-priority"), Queue("low-priority"))
    task_default_queue = "low-priority"
    task_default_exchange = "default"
    task_default_exchange_type = "direct"

    task_ignore_result = True

    # worker_send_task_event = False

    # task messages will be acknowledged after the task has been executed, not just before (the default behavior).
    task_acks_late = True
    # One worker taks 10 tasks from queue at a time and will increase the performance
    worker_prefetch_multiplier = 10

    if settings.app.env_mode == GenericSchema.EnvironmentMode.TEST:
        task_always_eager = True
