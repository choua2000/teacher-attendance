from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
class AttendanceSchema(BaseModel):
    teacher_id: str 
    classroom_id: str
    teacher_name: str
    teacher_date: dict 
    confidence: float
    time: str 
# 

# class AttendanceSchema(BaseModel):
#     teacher_id: str
#     classroom_id: str
#     name: str
#     teacher_date: dict
#     confidence: float
#     time: str
#     status: str
#     meeting_start: str
#     scan_time: str
#     late_minutes: int
class TeacherSchema(BaseModel):
    name: str
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    phone: str
    position: str
class ClassRoomSchema(BaseModel):
    title: str
    class_name: str
    class_hour: str
    class_time: str
class AttendanceWithTeacherSchema(BaseModel):
    teacher: TeacherSchema
    class_room: ClassRoomSchema
    teacher_date: dict
    confidence: float
    time: str
# class PredictAttendanceRequest(BaseModel):
#     class_room_id: str
class AttendanceListResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[AttendanceWithTeacherSchema]]