from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from pydantic_core.core_schema import ValidationInfo

example_min_quantity = None
example_max_quantity = 30
example_max_message = "Ya no puedes guardar más objetos de este tipo"
example_min_message = None
example_product_id = 2
example_user_id = 5


class AlertResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    read: bool = Field(examples=[False])
    min_quantity: Optional[int] = Field(None, examples=[example_min_quantity])
    max_quantity: Optional[int] = Field(None, examples=[example_max_quantity])
    max_message: Optional[str] = Field(None, examples=[example_max_message])
    min_message: Optional[str] = Field(None, examples=[example_min_message])
    product_id: int = Field(examples=[example_product_id])
    user_id: int = Field(examples=[example_user_id])


class CreateAlertSchema(BaseModel):
    read: bool = Field(examples=[False])
    min_quantity: Optional[int] = Field(None, examples=[example_min_quantity])
    max_quantity: Optional[int] = Field(None, examples=[example_max_quantity])
    max_message: Optional[str] = Field(None, examples=[example_max_message])
    min_message: Optional[str] = Field(None, examples=[example_min_message])
    product_id: int = Field(examples=[example_product_id])
    user_id: int = Field(examples=[example_user_id])


class UpdateAlertSchema(BaseModel):
    read: bool = Field(None, examples=[False])
    min_quantity: Optional[int] = Field(None, examples=[example_min_quantity])
    max_quantity: Optional[int] = Field(None, examples=[example_max_quantity])
    max_message: Optional[str] = Field(None, examples=[example_max_message])
    min_message: Optional[str] = Field(None, examples=[example_min_message])
    product_id: int = Field(None, examples=[example_product_id])
    user_id: int = Field(None, examples=[example_user_id])

    @model_validator(mode='before')
    def check_fields(cls, values: ValidationInfo):
        min_quantity = values.get('min_quantity', None)
        max_quantity = values.get('max_quantity', None)

        if min_quantity is not None and max_quantity is not None:
            raise ValueError('min_quantity and max_quantity cannot both be provided')

        if min_quantity is None and max_quantity is None:
            raise ValueError('At least one of min_quantity or max_quantity must be provided')

        return values
