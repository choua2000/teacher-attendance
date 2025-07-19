from app.backend.helper.attendance import attendance_helper, join_attendance_with_teacher
from typing import List, Optional
from fastapi import HTTPException, status
from app.backend.database.db import attendance_collection, teachers_collection, class_rooms_collection
from app.backend.models.attendance import AttendanceSchema, AttendanceWithTeacherSchema
from datetime import datetime, timedelta
from pymongo import DESCENDING
from bson import ObjectId
class AttendanceController:
    def __init__(self, collection):
        self.collection = collection
    # Retrieve attendance by teacher ID and date
    async def get_attendance_by_teacher_and_date(self, teacher_id: str, date: Optional[str] = None) -> dict:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        attendance = await self.collection.find_one({"teacher_id": teacher_id, "teacher_date": date})
        if not attendance:
            raise HTTPException(status_code=404, detail="ATTENDANCE_NOT_FOUND")
        
        return attendance_helper(attendance)

    # Add new attendance record
    async def add_attendance(self, attendance_data: AttendanceSchema) -> dict:
        existing = await self.collection.find_one({"teacher_id": attendance_data["teacher_id"], "teacher_date": attendance_data["teacher_date"],"classroom_id": attendance_data["classroom_id"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ATTENDANCE_ALREADY_EXISTS"
            )

        await self.collection.insert_one(attendance_data)
        new_attendance = await self.collection.find_one({"teacher_id": attendance_data["teacher_id"], "teacher_date": attendance_data["teacher_date"],"classroom_id": attendance_data["classroom_id"]})

        return {
            "message": "ATTENDANCE_ADDED_SUCCESSFULLY",
            "attendance": attendance_helper(new_attendance)
        }
    # get attendance all records
    async def get_all_attendance(self) -> List[dict]:
        attendance_records = await self.collection.find().sort("teacher_date", DESCENDING).to_list(length=None)
        return [attendance_helper(record) for record in attendance_records]
    
    # get attendance by to join teacher
    async def get_attendance_with_teacher(self) -> List[AttendanceWithTeacherSchema]:
        attendances = await self.collection.find({}).to_list(length=None)
        results = []

        for att in attendances:
            teacher = await teachers_collection.find_one({"_id": ObjectId(att["teacher_id"])})
            classroom = await class_rooms_collection.find_one({"_id": ObjectId(att["classroom_id"])})
            if teacher and classroom: 
                results.append(join_attendance_with_teacher(att, teacher, classroom))

        return results
    # get teacher by name
    async def get_teacher_by_name(self, name: str) -> dict:
        print(f"name class: {name}")

        if not name:
            raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND0000")
        return await self.collection.find_one({"first_name": name})
   # delete attendance
    async def delete_attendance(self, attendance_id: str):
     if not ObjectId.is_valid(attendance_id):
        raise HTTPException(status_code=404, detail="ATTENDANCE_NOT_FOUND")

     attendance = await self.collection.find_one({"_id": ObjectId(attendance_id)})
     if not attendance:
        return None

     deleted_result = await self.collection.delete_one({"_id": ObjectId(attendance_id)})
     if deleted_result.deleted_count == 0:
        return None
     attendance["_id"] = str(attendance["_id"])
     return attendance  # คืน document เต็ม ๆ

attendance_controller = AttendanceController(attendance_collection)