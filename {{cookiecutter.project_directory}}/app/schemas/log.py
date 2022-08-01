from typing import Optional, Dict
from pydantic import BaseModel, Field

# Schemas
from app.schemas.generic import EnvironmentMode


class EcsBaseLogSchema(BaseModel):
    path: Optional[str] = Field(None)
    method: Optional[str] = Field(None)
    request_body: Optional[Dict] = Field(None)
    response_body: Optional[Dict] = Field(None)
    response_status_code: Optional[int] = Field(None)
    x_real_ip: Optional[str] = Field(None)
    x_error: Optional[str] = Field(None)


class EcsInitializeLogSchema(EcsBaseLogSchema):
    provider: str
    env_mode: EnvironmentMode

    class Config:
        user_enum_values = True
