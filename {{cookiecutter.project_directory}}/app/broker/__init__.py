import celery
import sentry_sdk
from celery import current_app as current_celery_app
from celery.signals import worker_process_init
from sentry_sdk.integrations.celery import CeleryIntegration
from typing import Any
from loguru import logger

###
from app import __VERSION__
from app.config import CeleryConfiguration, settings


# Inititalize
@worker_process_init.connect
def worker_initialize(*args: Any, **kwargs: Any) -> None:
    logger.info("--- Worker initialize ...")
    if settings.sentry.dns:
        sentry_sdk.init(
            settings.sentry.dns,
            traces_sample_rate=settings.sentry.trace_sample_rates,
            release=f"{settings.app.application_name}-worker@{__VERSION__}",
            environment=settings.app.env_mode.value,
            integrations=[CeleryIntegration()],
        )


def create_celery() -> celery:
    celery_app = current_celery_app
    celery_app.config_from_object(CeleryConfiguration)

    return celery_app
