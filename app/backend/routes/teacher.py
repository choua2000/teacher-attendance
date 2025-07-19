from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from app.backend.models.teacher import TeacherSchema
from app.backend.controllers.teacher import teacher_controller
from app.backend.controllers.admin import admin_controller
from app.backend.helper.index import ResponseRegister, ResponseLogin

router = APIRouter()

@router.post("/teacher", response_description="Register a new teacher")
async def register_teacher(teacher: TeacherSchema = Body(...)):
    teacher_data = jsonable_encoder(teacher)
    result = await teacher_controller.teacher_register(teacher_data)
    return {
        "teacher": result["teacher"],
        "message": result["message"]
    }


