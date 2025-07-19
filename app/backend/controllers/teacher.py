from fastapi import HTTPException, status
from app.backend.database.db import teachers_collection
from app.backend.helper.teacher import teacher_helper
from datetime import datetime, timedelta
import uuid, bcrypt, jwt
from bson import ObjectId
SECRET_KEY = "CHOUA12345"

class TeacherController:
    def __init__(self, collection):
        self.collection = collection

    async def teacher_register(self, teacher_data: dict) -> dict:
     existing = await self.collection.find_one({"email": teacher_data["email"]})
     if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="USER_ALREADY_EXISTS"
        )

    #  print("🟢 Inserting teacher data:", teacher_data)  # log input

     result = await self.collection.insert_one(teacher_data)

     new_teacher = await self.collection.find_one({"_id": result.inserted_id})
     if not new_teacher:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve teacher after registration"
        )

    #  print("✅ Retrieved teacher:", new_teacher)

     return {
        "message": "TEACHER_REGISTERED_SUCCESSFULLY",
        "teacher": teacher_helper(new_teacher)
    }

   # Update teacher information
    async def update_teacher(self, teacher_id: str, update_data: dict):
        if len(update_data) < 1:
            return False
        
        result = self.collection.find_one({"_id":ObjectId(teacher_id) })
        if result:
            updated_teacher = await self.collection.update_one(
                {"_id": ObjectId(teacher_id)},
                {"$set": update_data}
            )
            if updated_teacher.modified_count > 0:
                return True
            return False

    # Delete teacher
    async def delete_teacher(self, teacher_id: str):
        if not ObjectId.is_valid(teacher_id):
            raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")
        result = self.collection.find_one({"_id":ObjectId(teacher_id) })
        if result:
            deleted_teacher = await self.collection.delete_one({"_id": ObjectId(teacher_id)})
            if deleted_teacher.deleted_count > 0:
                return True
            return False
    # Get one teacher by ID
    async def get_teacher_id(self, teacher_id: str):
        if not ObjectId.is_valid(teacher_id):
            raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")
        teacher = await self.collection.find_one({"_id": ObjectId(teacher_id)})
        if teacher:
            return teacher_helper(teacher)
        raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")
    # Get all teachers
    async def get_all_teachers(self):
        teachers = []
        async for teacher in self.collection.find():
            teachers.append(teacher_helper(teacher))
        return teachers
    
    async def get_teacher_by_name(self, name: str) -> dict:
        print(f"name class: {name}")

        if not name:
            raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND0000")
        return await self.collection.find_one({"name": name})


teacher_controller = TeacherController(teachers_collection)
