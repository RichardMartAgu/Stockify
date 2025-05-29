from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

example_name = "Ordenador"
example_quantity = 12
example_serial_number = "A123456"
example_price = 230.50
example_description = "Ordenador clase media"
example_category = "Ordenadores"
kit_id = 5
example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"


class ProductResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    kit_id: Optional[int] = Field(examples=[kit_id])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class CreateProductSchema(BaseModel):
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    kit_id: Optional[int] = Field(examples=[kit_id])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class UpdateProductSchema(BaseModel):
    name: str = Field(None, examples=[example_name])
    quantity: int = Field(None, examples=[example_quantity])
    serial_number: str = Field(None, examples=[example_serial_number])
    price: float = Field(None, examples=[example_price])
    description: Optional[str] = Field(None, examples=[example_description])
    category: Optional[str] = Field(None, examples=[example_category])
    kit_id: Optional[int] = Field(None, examples=[kit_id])
    image_url: Optional[str] = Field(None, examples=[example_image_url])
    warehouse_id: int = Field(None, examples=[3])


# Relationship schemas
# Product products schemas
class ProductsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class ProductProductsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])
    products: Optional[List[ProductsBase]]


# Product transactions schemas
class TransactionsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=["in"])
    warehouse_id: Optional[int] = Field(examples=[3])
    client_id: Optional[int] = Field(examples=[5])


class ProductTransactionsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    kit_id: Optional[int] = Field(None, examples=[kit_id])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])
    transactions: Optional[List[TransactionsBase]]


# Product alerts schemas
class AlertsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    read: bool = Field(examples=[False])
    min_quantity: Optional[int] = Field(None, examples=[None])
    max_quantity: Optional[int] = Field(None, examples=[30])
    max_message: Optional[str] = Field(None, examples=["Ya no puedes guardar más objetos de este tipo"])
    min_message: Optional[str] = Field(None, examples=[None])
    product_id: int = Field(examples=[2])


class ProductAlertsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: float = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    kit_id: Optional[int] = Field(None, examples=[kit_id])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])
    alerts: Optional[List[AlertsBase]]
