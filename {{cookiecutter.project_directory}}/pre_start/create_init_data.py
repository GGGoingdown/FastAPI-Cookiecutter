import sys
import os
from pathlib import Path
from loguru import logger
from tortoise import run_async


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # app folder
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


###
from app import models  # noqa: E402
from app.schemas import UserSchema  # noqa: E402
from app.services.auth import BaseAuthService  # noqa: E402


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
        password_hash = BaseAuthService.get_password_hash(user_payload.password)
        user_model = models.User(
            password_hash=password_hash,
            **user_payload.dict(exclude={"password", "verify_password"}),
        )
        await user_model.save()

        await models.User.get(id=user_model.id)
        logger.info("--- Create user successful ---")


async def main():
    try:
        from app.containers import Application
        from pre_start.check_connection import db_connected

        container = Application()
        logger.info("--- Connect DB ---")
        await container.gateway.db_resource.init()
        logger.info("--- Check DB connection---")
        await db_connected()
        logger.info("--- Get admin information ---")
        admin_info = get_admin_info()
        logger.info("--- Create admin ---")
        await create_user(admin_info)

    finally:
        await container.gateway.db_resource.shutdown()


if __name__ == "__main__":
    run_async(main())
