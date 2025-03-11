from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(..., examples=["Pepe"])
    email: EmailStr = Field(..., examples=["pepe@gmail.com"])
    role: str = Field(..., examples=["Admin"])
    admin_id: Optional[int] = Field(examples=[3])


class CreateUserSchema(BaseModel):
    username: Optional[str] = Field(..., example="Pepe")
    password: Optional[str] = Field(..., example="123456")
    email: Optional[EmailStr] = Field(..., example="pepe@gmail.com")
    role: str = Field(..., examples=["Admin"])
    admin_id: Optional[int] = Field(examples=["null"])


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, example="Pepe")
    password: Optional[str] = Field(None, example="123456")
    email: Optional[EmailStr] = Field(None, example="pepe@gmail.com")
    role: str = Field(None, examples=["Admin"])
    admin_id: Optional[int] = Field(examples=["null"])
