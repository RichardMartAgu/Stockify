from typing import Optional

from pydantic import BaseModel, Field, EmailStr

example_name = "Pepe"
example_password = "123456"
example_email = "pepe@gmail.com"
example_role = "Admin"
example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"


class UserResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    image_url: Optional[str] = Field(examples=[example_image_url])
    admin_id: Optional[int] = Field(examples=[3])


class CreateUserSchema(BaseModel):
    username: str = Field(examples=[example_name])
    password: str = Field(examples=[example_password])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    image_url: Optional[str] = Field(examples=[example_image_url])
    admin_id: Optional[int] = Field(examples=["null"])


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, examples=[example_name])
    password: Optional[str] = Field(None, examples=[example_password])
    email: Optional[EmailStr] = Field(None, examples=[example_email])
    role: Optional[str] = Field(None, examples=[example_role])
    image_url: Optional[str] = Field(None, examples=[example_image_url])
    admin_id: Optional[int] = Field(None, examples=["null"])
