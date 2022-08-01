import shortuuid
from datetime import datetime


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(microsecond=0)


def get_shortuuid() -> str:
    return shortuuid.uuid()
