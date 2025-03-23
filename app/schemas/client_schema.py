from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

example_identifier = "1233456B"
example_name = "TiendaSA"
example_email = "tiendaSA@gmail.com"
example_contact = "Juanito"
example_phone = "123456789"
example_address = "AV/Sin nombre nº3"


class ClientResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: str = Field(examples=[example_identifier])
    name: str = Field(examples=[example_name])
    contact: Optional[str] = Field(examples=[example_contact])
    phone: Optional[str] = Field(examples=[example_phone])
    email: Optional[EmailStr] = Field(examples=[example_email])
    address: Optional[str] = Field(examples=[example_address])


class CreateClientSchema(BaseModel):
    identifier: str = Field(examples=[example_identifier])
    name: str = Field(examples=[example_name])
    contact: Optional[str] = Field(examples=[example_contact])
    phone: Optional[str] = Field(examples=[example_phone])
    email: Optional[EmailStr] = Field(examples=[example_email])
    address: Optional[str] = Field(examples=[example_address])


class UpdateClientSchema(BaseModel):
    identifier: str = Field(examples=[example_identifier])
    name: str = Field(examples=[example_name])
    contact: Optional[str] = Field(None, examples=[example_contact])
    phone: Optional[str] = Field(None, examples=[example_phone])
    email: Optional[EmailStr] = Field(None, examples=[example_email])
    address: Optional[str] = Field(None, examples=[example_address])

# Relationship schemas
# Client transactions schemas
class TransactionsBase(BaseModel):
    id: Optional[int] = Field(examples=[5])
    date: datetime = Field(examples=["2024-03-16T14:30:00"])
    type: str = Field(examples=["in"])
    warehouse_id: Optional[int] = Field(examples=[3])
    client_id: Optional[int] = Field(examples=[5])

class ClientTransactionsResponseSchema(BaseModel):
    id: Optional[int] = Field(examples=[5])
    identifier: str = Field(examples=[example_identifier])
    name: str = Field(examples=[example_name])
    contact: Optional[str] = Field(examples=[example_contact])
    phone: Optional[str] = Field(examples=[example_phone])
    email: Optional[EmailStr] = Field(examples=[example_email])
    address: Optional[str] = Field(examples=[example_address])
    transactions: Optional[List[TransactionsBase]]
