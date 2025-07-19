# from pydantic import BaseModel, Field, EmailStr
# from typing import Optional

# class ReportSchema(BaseModel):
#     attendance_id: str
#     title: str = Field(...)
#     class_name: str = Field(...)
#     hour: str = Field(...)
#     time: str

from pydantic import BaseModel, Field
from typing import Dict

class AttendanceSchema(BaseModel):
    teacher_id: str
    teacher_date: Dict[str, str]
    confidence: float
    time: str

class ReportSchema(BaseModel):
    id: str
    attendance_id: str
    title: str
    class_name: str
    hour: str
    time: str
    attendance: AttendanceSchema
