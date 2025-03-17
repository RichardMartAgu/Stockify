from typing import Optional, List

from pydantic import BaseModel, Field
from sqlalchemy import DateTime

example_product_id = 3
example_quantity = 5

example_type = "in"
example_warehouse_id = 3
example_client_id = 5


class ProductTransaction(BaseModel):
    product_id: int = Field(examples=[example_product_id])
    quantity: int = Field(examples=[example_quantity])


class TransactionResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: str = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=[example_type])
    warehouse_id: Optional[int] = Field(examples=[example_warehouse_id])
    client_id: Optional[int] = Field(examples=[example_client_id])
    products: List[ProductTransaction]


class CreateTransactionSchema(BaseModel):
    type: str = Field(examples=[example_type])
    warehouse_id: Optional[int] = Field(examples=[example_warehouse_id])
    client_id: Optional[int] = Field(examples=[example_client_id])
    products: List[ProductTransaction]
