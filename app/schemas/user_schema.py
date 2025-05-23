from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

example_name = "Pepe"
example_password = "123456"
example_email = "pepe@gmail.com"
example_role = "Admin"
stripe_subscription_status = "false"
example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"


class UserResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    stripe_subscription_status: bool = Field(examples=[stripe_subscription_status])
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

# Relationship schemas
# User employees schemas
class EmployeesBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])

class UserEmployeesResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    users: Optional[List[EmployeesBase]]

# User warehouses schemas
class WarehousesBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=["Almacén principal"])
    address: str = Field(examples=["Finca empresarial el unicornio nave 34"])
    phone: str = Field(examples=["666555444"])

class UserWarehousesResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    warehouses: Optional[List[WarehousesBase]]

# User clients schemas
class ClientsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: str = Field(examples=['1233456B'])
    name: str = Field(examples=['TiendaSA'])
    contact: Optional[str] = Field(examples=["tiendaSA@gmail.com"])
    phone: Optional[str] = Field(examples=["Juanito"])
    email: Optional[EmailStr] = Field(examples=["123456789"])
    address: Optional[str] = Field(examples=["AV/Sin nombre nº3"])
    user_id: int = Field(examples=["1"])

class UserClientsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    clients: Optional[List[ClientsBase]]

# User alerts schemas
class AlertsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    read: bool = Field(examples=[False])
    min_quantity: Optional[int] = Field(None, examples=[None])
    max_quantity: Optional[int] = Field(None, examples=[30])
    max_message: Optional[str] = Field(None, examples=["Ya no puedes guardar más objetos de este tipo"])
    min_message: Optional[str] = Field(None, examples=[None])
    product_id: int = Field(examples=[2])

class UserAlertsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    username: str = Field(examples=[example_name])
    email: EmailStr = Field(examples=[example_email])
    role: str = Field(examples=[example_role])
    alerts: Optional[List[AlertsBase]]