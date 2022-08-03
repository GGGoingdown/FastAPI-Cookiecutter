from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm


###
from app import services, responses
from app.containers import Application
from app.schemas import AuthSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/jwt",
    response_model=AuthSchema.LoginResponse,
    responses={401: responses.INCORRECT_USERNAME_OR_PASSWORD_EXAMPLE()},
)
@inject
async def create_jwt_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authentication_service: services.AuthenticationService = Depends(
        Provide[Application.service.authentication_service]
    ),
    authorization_service: services.AuthorizationService = Depends(
        Provide[Application.service.authorization_service]
    ),
):
    user_in_db = await authentication_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )

    jwt_token = authorization_service.create_jwt_token(user_id=user_in_db.id)

    return {"access_token": jwt_token, "token_type": "bearer"}
