import sentry_sdk
from typing import Dict, Any
from loguru import logger
from celery.signals import worker_process_init
from sentry_sdk.integrations.celery import CeleryIntegration

# from loguru import logger
from celery import shared_task


###
from app import __VERSION__
from app.config import settings

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


#################################################################################
#                   Health Check
#################################################################################
@shared_task()
def health_check() -> Dict:
    return {"detail": "health"}
