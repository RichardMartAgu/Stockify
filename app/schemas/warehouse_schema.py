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

class ProductBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=["Ordenador"])
    quantity: int = Field(examples=[12])
    serial_number: str = Field(examples=["A123456"])
    price: float = Field(examples=[230.50])
    description: Optional[str] = Field(examples=["Ordenador clase media"])
    category: Optional[str] = Field(examples=["Ordenadores"])
    kit_id: Optional[int] = Field(examples=[5])
    image_url: Optional[str] = Field(examples=[example_image_url])
    warehouse_id: int = Field(examples=[3])


class TransactionProductBase(BaseModel):
    quantity: int = Field(examples=[5])
    product: ProductBase


class TransactionsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: str = Field(examples=["A23232024"])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=["in"])
    warehouse_id: int = Field(examples=[3])
    client_id: int = Field(examples=[5])
    products: List[TransactionProductBase] = []


class WarehouseTransactionsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    name: str = Field(examples=["Warehouse A"])
    address: str = Field(examples=["123 Warehouse St."])
    phone: str = Field(examples=["123-456-7890"])
    user_id: int = Field(examples=[3])
    transactions: List[TransactionsBase]


warehouse_example = {
    "example": {
        "id": 5,
        "name": "Warehouse A",
        "address": "123 Warehouse St.",
        "phone": "123-456-7890",
        "user_id": 3,
        "transactions": [
            {
                "id": 5,
                "identifier": "A23232024",
                "date": "2024-03-16T14:30:00",
                "type": "in",
                "warehouse_id": 3,
                "client_id": 5,
                "products": [
                    {
                        "quantity": 5,
                        "product": {
                            "id": 5,
                            "name": "Ordenador",
                            "quantity": 12,
                            "serial_number": "A123456",
                            "price": 230.50,
                            "description": "Ordenador clase media",
                            "category": "Ordenadores",
                            "kit_id": 5,
                            "image_url": "https://example.com/image.jpg",
                            "warehouse_id": 3
                        }
                    }
                ]
            }
        ]
    }
}