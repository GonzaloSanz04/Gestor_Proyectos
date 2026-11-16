
from pydantic import Field, BaseModel


class LoginRequest(BaseModel):
    identificador: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=72)


class Token(BaseModel):
    access_token: str = Field()
    token_type: str = Field(default="bearer")
    