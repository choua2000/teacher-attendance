from pydantic import BaseModel, EmailStr
from typing import Optional
# teacher schema for registration and login
class TeacherSchema(BaseModel):
    # classroom_id: str
    name: str
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    phone: str
    position: str

    

class UpdateTeacherModel(BaseModel):
    # name: str
    first_name: str
    last_name:str
    email: EmailStr
    age: int
    phone: str
    position: str

class UpdateByAdminModel(BaseModel):
    # name: Optional[str]
    first_name: Optional[str]
    last_name:Optional[str]
    email: Optional[EmailStr]
    age: Optional[int] 
    phone: Optional[str] 
    position: Optional[str] 

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Jane Doe",
    #             "last_name": "Smith",
    #             "email": "gWV8a@example.com",
    #             "age": 25,
    #             "phone": "9876543210",
    #             "position": "Senior Teacher"
    #         }
    #     }