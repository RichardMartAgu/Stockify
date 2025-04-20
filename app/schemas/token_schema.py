from pydantic import BaseModel, Field, EmailStr

example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"

class TokenResponse(BaseModel):
    access_token: str = Field(examples=["token"])
    token_type: str = Field(examples=["barer"])
    username: str = Field(examples=["Pepe"])
    email: EmailStr = Field(examples=["pepe@gmail.com"])
    id: int = Field(examples=[5])
    image_url: str = Field(examples=[example_image_url])

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None
