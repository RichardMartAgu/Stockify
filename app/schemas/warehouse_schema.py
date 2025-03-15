from typing import Optional

from pydantic import BaseModel, Field

example_name = "Almacén principal"
example_address = "Finca empresarial el unicornio nave 34 "
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