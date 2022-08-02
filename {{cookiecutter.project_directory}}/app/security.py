from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from dependency_injector.wiring import inject, Provide

###
from app import services
from app.containers import Application
from app.schemas import AuthSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@inject
async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    authentication_service: services.AuthenticationService = Depends(
        Provide[Application.service.authentication_service]
    ),
) -> AuthSchema.JWTUser:
    return authentication_service.authenticate_jwt(security_scopes, token=token)
