from pydantic import BaseModel, Field , EmailStr

class ClassNameSchema(BaseModel):
    class_name: str = Field(...)