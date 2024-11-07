from datetime import date

from pydantic import BaseModel, Field, EmailStr


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(max_length=10)
    birthday: date = Field(None)
    description: str = Field(None, max_length=300)


class ContactCreateSchema(ContactSchema):
    pass


class ContactUpdateSchema(ContactSchema):
    name: str = Field(None, min_length=2, max_length=100)
    email: EmailStr = Field(None)
    phone: str = Field(None, max_length=10)
    birthday: date = Field(None)
    description: str = Field(None, max_length=300)

class ContactResponseSchema(ContactSchema):
    id: int

    class Config:
        orm_mode = True
