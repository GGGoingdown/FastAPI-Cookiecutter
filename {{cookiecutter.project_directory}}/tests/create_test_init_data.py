import sys
from loguru import logger
from tortoise import run_async
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # app folder
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

###
# Application
###
from app import models  # noqa: E402
from app.schemas import UserSchema  # noqa: E402
from app.services.auth import BaseAuthService  # noqa: E402
from tests import fake_data  # noqa: E402


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
        logger.info("--- Get test user information ---")
        test_user_info = fake_data.get_test_user_info()
        logger.info("--- Create test user ---")
        await create_user(test_user_info)

    finally:
        await container.gateway.db_resource.shutdown()


if __name__ == "__main__":
    run_async(main())
