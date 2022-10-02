from typing import Dict

# from loguru import logger
from celery import shared_task

# from dependency_injector.wiring import inject, Provide

###
# from app import services
# from app.containers import Application

#################################################################################
#                   Health Check
#################################################################################
@shared_task()
def health_check() -> Dict:
    return {"detail": "health"}
