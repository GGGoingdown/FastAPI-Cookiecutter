import sys
import os
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


def get_test_user_info() -> UserSchema.CreateUser:
    name = os.environ.get("test_user", "test_user")
    mail = os.environ.get("test_user_email", "test_user@gmail.com")
    password = os.environ.get("test_user_password", "test123")

    return UserSchema.CreateUser(
        name=name, email=mail, password=password, verify_password=password
    )


async def get_user_model(email: str):
    return await models.User.get(email=email)
