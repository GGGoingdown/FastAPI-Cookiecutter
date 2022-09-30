import sys
import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # app folder
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


import traceback  # noqa: E402
from tortoise import Tortoise, run_async  # noqa: E402
from tenacity import retry, stop_after_attempt, wait_fixed  # noqa: E402
from loguru import logger  # noqa: E402

###
from app import models  # noqa: E402
from app.containers import Application  # noqa: E402
from app.schemas import UserSchema  # noqa: E402


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(stop=stop_after_attempt(max_tries), wait=wait_fixed(wait_seconds))
async def db_connected():
    try:
        conn = Tortoise.get_connection("default")
        logger.info(f"Ping -> {await conn.execute_query('SELECT 1')}")

    except ConnectionRefusedError as e:
        error_message = traceback.format_exc()
        logger.error(error_message)
        raise e

    except Exception as e:
        error_message = traceback.format_exc()
        logger.error(error_message)
        raise e


def get_admin_info() -> UserSchema.CreateUser:
    name = os.environ.get("admin", "admin")
    mail = os.environ.get("admin_email", "admin@gmail.com")
    password = os.environ.get("admin_password", "admin")

    return UserSchema.CreateUser(
        name=name, email=mail, password=password, verify_password=password
    )


async def create_user(user_payload: UserSchema.CreateUser):
    if user_model := await models.User.filter(email=user_payload.email).first():
        logger.info("--- Already create user ---")
    else:
        logger.info("--- Create user ---")
        user_model = models.User(**user_payload.dict())
        await user_model.save()

        await models.User.get(id=user_model.id)
        logger.info("--- Create user successful ---")


async def main():
    try:
        container = Application()
        logger.info("--- Connect DB ---")
        await container.gateway.db_resource.init()
        await db_connected()
        logger.info("--- Get admin information ---")
        admin_info = get_admin_info()
        logger.info("--- Create admin ---")
        await create_user(admin_info)

    finally:
        await container.gateway.db_resource.shutdown()


if __name__ == "__main__":
    run_async(main())
