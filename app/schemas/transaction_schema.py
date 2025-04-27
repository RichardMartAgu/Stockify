from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

example_product_id = 3
example_quantity = 5

example_type = "in"
example_identifier = "A23232024"
example_warehouse_id = 3
example_client_id = 5


class TransactionResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: Optional[str] = Field(examples=[example_identifier])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=[example_type])
    warehouse_id: Optional[int] = Field(examples=[example_warehouse_id])
    client_id: Optional[int] = Field(examples=[example_client_id])


# Relationship schemas

class ProductTransaction(BaseModel):
    product_id: int = Field(examples=[example_product_id])
    quantity: int = Field(examples=[example_quantity])


class CreateTransactionSchema(BaseModel):
    type: str = Field(examples=[example_type])
    warehouse_id: Optional[int] = Field(examples=[example_warehouse_id])
    client_id: Optional[int] = Field(examples=[example_client_id])
    products: List[ProductTransaction]


# Product transactions schemas
class TransactionProductsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: Optional[str] = Field(examples=[example_identifier])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=[example_type])
    warehouse_id: Optional[int] = Field(examples=[example_warehouse_id])
    client_id: Optional[int] = Field(examples=[example_client_id])
    products: List[ProductTransaction]
