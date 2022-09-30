from pydantic import BaseModel, EmailStr, Field, validator


class UserMail(BaseModel):
    email: EmailStr


class CreateUser(UserMail):
    name: str = Field()
    password: str = Field()
    verify_password: str = Field()

    @validator("name")
    def check_name_length(cls, v):
        if len(v) > 50:
            raise ValueError("Too many characters")
        return v

    @validator("password", "verify_password")
    def check_length(cls, v):
        if len(v) > 128:
            raise ValueError("Too many characters")
        return v

    @validator("verify_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserInDB(UserMail):
    id: int = Field(..., description="User ID in DB")
    name: str = Field()

    class Config:
        orm_mode = True
