from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AdminSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    age: int = Field(...)
    phone: str = Field(...)
    role: str = "admin"

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "fullname": "John Doe",
    #             "email": "6cE0z@example.com",
    #             "password": "password123",
    #             "age": 30,
    #             "phone": "1234567890",
    #             "role": "admin"
    #         }
    #     }



class AdminLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    