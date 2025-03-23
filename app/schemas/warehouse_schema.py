from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, condecimal

example_name = "Almacén principal"
example_address = "Finca empresarial el unicornio nave 34"
example_phone = "666555444"


class WarehouseResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    address: Optional[str] = Field(examples=[example_phone])
    phone: Optional[str] = Field(examples=[example_phone])
    user_id: Optional[int] = Field(examples=[3])


class CreateWarehouseSchema(BaseModel):
    name: str = Field(examples=[example_name])
    address: Optional[str] = Field(examples=[example_address])
    phone: Optional[str] = Field(examples=[example_phone])
    user_id: Optional[int] = Field(examples=[5])


class UpdateWarehouseSchema(BaseModel):
    name: Optional[str] = Field(None, examples=[example_name])
    address: Optional[str] = Field(None, examples=[example_address])
    phone: Optional[str] = Field(None, examples=[example_phone])

# Relationship schemas
# Warehouse products schemas

example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"

class ProductsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=["Ordenador"])
    price: condecimal(max_digits=10, decimal_places=2) = Field(examples=[230.50])
    category: Optional[str] = Field(examples=["Ordenadores"])
    image_url: Optional[str] = Field(examples=[example_image_url])

class WarehouseProductsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    address: Optional[str] = Field(examples=[example_phone])
    phone: Optional[str] = Field(examples=[example_phone])
    user_id: Optional[int] = Field(examples=[3])
    products: Optional[List[ProductsBase]]

# Warehouse transactions schemas

class TransactionsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=["in"])
    warehouse_id: Optional[int] = Field(examples=[3])
    client_id: Optional[int] = Field(examples=[5])

class WarehouseTransactionsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    address: Optional[str] = Field(examples=[example_phone])
    phone: Optional[str] = Field(examples=[example_phone])
    user_id: Optional[int] = Field(examples=[3])
    transactions: Optional[List[TransactionsBase]]