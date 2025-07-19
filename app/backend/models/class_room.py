# from pydantic import BaseModel, Field, EmailStr
# class ClassRoomSchema(BaseModel):
#     title: str 
#     class_name: str 
#     class_hour: str 
#     data: list
# class ClassRoomUpdateSchema(BaseModel):
#     title: str = Field(...)
#     class_name: str = Field(...)
#     class_hour: int = Field(...)
#     data: list

from pydantic import BaseModel, Field
from typing import List, Union, Optional

class ClassRoomSchema(BaseModel):
    title: str = Field(...)
    class_name: str = Field(...)
    class_hour: str = Field(...)
    class_time: str = Field(...) # or List[dict] depending on what you store

class ClassRoomUpdateSchema(BaseModel):
    title: Optional[str] = None
    class_name: Optional[str] = None
    class_hour: Optional[Union[int, str]] = None
    class_time: Optional[str] = None  # same as above
