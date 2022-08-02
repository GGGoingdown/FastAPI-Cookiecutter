import pytest
from unittest import mock

###
#   Application
###
from app import repositories
from tests import fake_data

ENDPOINT = "/auth/jwt"

test_user_info = fake_data.get_test_user_info()


@pytest.mark.auth
@pytest.mark.asyncio
async def test_auth_jwt(client, app):
    # Get user model
    user_model = await fake_data.get_user_model(email=test_user_info.email)

    user_repo_mock = mock.AsyncMock(spec=repositories.UserRepo)
    user_repo_mock.filter_by_mail.return_value = user_model

    with app.container.service.user_repo.override(user_repo_mock):
        r = client.post(
            ENDPOINT,
            data={"username": test_user_info.name, "password": test_user_info.password},
            headers={"Content Type": "application/x-www-form-urlencoded"},
        )

    assert r.status_code == 200, f"Error status code: {r.json()}"
