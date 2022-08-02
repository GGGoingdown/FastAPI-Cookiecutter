from fastapi import APIRouter, Depends

###
from app import security
from app.schemas import AuthSchema


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me", include_in_schema=False, response_model=AuthSchema.JWTUser)
async def get_me(current_user: AuthSchema.JWTUser = Depends(security.get_current_user)):
    return current_user
