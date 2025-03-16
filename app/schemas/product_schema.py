from typing import Optional

from pydantic import BaseModel, Field, EmailStr, condecimal

example_name = "Ordenador"
example_quantity = 12
example_serial_number = "A123456"
example_price = 230.50
example_description = "Ordenador clase media"
example_category = "Ordenadores"
example_image_url = "https://stockifystorage.s3.us-east-1.amazonaws.com/user_profiles/Flux_Dev_A_stylized_icon_for_a_modern_storage_company_featurin_1.jpeg"


class ProductResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: condecimal(max_digits=10, decimal_places=2) = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class CreateProductSchema(BaseModel):
    name: str = Field(examples=[example_name])
    quantity: int = Field(examples=[example_quantity])
    serial_number: str = Field(examples=[example_serial_number])
    price: condecimal(max_digits=10, decimal_places=2) = Field(examples=[example_price])
    description: Optional[str] = Field(examples=[example_description])
    category: Optional[str] = Field(examples=[example_category])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class UpdateProductSchema(BaseModel):
    name: str = Field(None,examples=[example_name])
    quantity: int = Field(None,examples=[example_quantity])
    serial_number: str = Field(None,examples=[example_serial_number])
    price: condecimal(max_digits=10, decimal_places=2) = Field(None,examples=[example_price])
    description: Optional[str] = Field(None,examples=[example_description])
    category: Optional[str] = Field(None,examples=[example_category])
    image_url: Optional[str] = Field(None,examples=[example_image_url])
    warehouse_id: int = Field(None,examples=[3])
