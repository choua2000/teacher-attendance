from pydantic import BaseModel, Field, EmailStr
from typing import Optional
class PositionSchema(BaseModel):
    room_id: str 
    room_name: str
    hour: str
     # Optional field for confidence score