import celery
from celery import current_app as current_celery_app

###
from app.config import CeleryConfiguration


def create_celery() -> celery:
    celery_app = current_celery_app
    celery_app.config_from_object(CeleryConfiguration)

    return celery_app
