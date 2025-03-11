from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(examples=["token"])
    token_type: str = Field(examples=["barer"])

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
