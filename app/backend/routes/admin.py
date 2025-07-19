from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from app.backend.models.admin import AdminSchema, AdminLoginSchema
from app.backend.models.teacher import UpdateByAdminModel
from app.backend.controllers.admin import admin_controller
from app.backend.controllers.teacher import teacher_controller
from app.backend.helper.index import( ResponseRegister,ResponseModels, ResponseLogin, ResponseUpdateTeacher, verify_jwt_token_and_role, ErrorResponseModel)

router = APIRouter()
# Admin Register Teacher
@router.post("/admin_register", response_description="Register a new teacher")
async def admin_register(teacher: AdminSchema = Body(...)):
    teacher_data = jsonable_encoder(teacher)
    result = await admin_controller.admin_register(teacher_data)
    return ResponseRegister(result["admin"], result["message"])
# Admin Login
@router.post("/admin_login", response_description="routes Admin Login")
async def admin_login(admin: AdminLoginSchema = Body(...)):
    admin = jsonable_encoder(admin)
    token,admin,message = await admin_controller.admin_login(admin)
    return ResponseLogin(token,admin,message)

# Admin Update Teacher
@router.put("/update/{teacher_id}", response_description="Update teacher ")
async def update_teacher(teacher_id: str, teacher:UpdateByAdminModel = Body(...)):
    teacher = {k: v for k, v in teacher.dict().items() if v is not None}
    if len(teacher) >= 1:
        update_teacher_data = await teacher_controller.update_teacher(teacher_id, teacher)
        # print(f"update_teacher_data",update_teacher_data)
        if update_teacher_data:
            return ResponseUpdateTeacher("Teacher updated successfully by admin:{0}".format(teacher_id), "TEACHER_UPDATED_SUCCESSFULLY")
        else:
            return ErrorResponseModel(
                error="Failed to update teacher {0}".format(teacher_id),
                code="TEACHER_UPDATE_FAILED",
                message="Unable to update teacher data. Please check the input and try again.")
# Admin Delete Teacher
@router.delete("/delete/{teacher_id}", response_description="Delete teacher")
async def delete_teacher(teacher_id: str):
    teacher = await teacher_controller.delete_teacher(teacher_id)
    if teacher:
        return ResponseUpdateTeacher("Teacher deleted successfully by admin:{0}".format(teacher_id), "TEACHER_DELETED_SUCCESSFULLY")
    else:
        return ErrorResponseModel("Failed to delete teacher{0}".format(teacher_id),404, "TEACHER_DELETE_FAILED")
# Admin Get one Teachers
@router.get("/get_id/{teacher_id}", response_description="Get one teacher")
async def get_teacher_id(teacher_id: str):
    teacher = await teacher_controller.get_teacher_id(teacher_id)
    if teacher:
        return ResponseUpdateTeacher(teacher, "TEACHER_FOUND_SUCCESSFULLY")
    else:
        return ErrorResponseModel("Failed to find teacher{0}".format(teacher_id),404, "TEACHER_NOT_FOUND")
# Admin Get all Teachers
@router.get("/get_all_teachers", response_description="Get all teachers")
# async def get_all_teachers(payload: dict = Depends(verify_jwt_token_and_role)):
async def get_all_teachers():
    teachers = await teacher_controller.get_all_teachers()
    if teachers:
        return ResponseUpdateTeacher(teachers, "TEACHERS_FOUND_SUCCESSFULLY")
    else:
        return ErrorResponseModel(
            data=None,
            message="Failed to find teachers",
            error="TEACHERS_NOT_FOUND"
)
    
# Admin Get all Admins
@router.get("/get_admins", response_description="Get all admins")
async def get_all_admins():
    admins = await admin_controller.get_all_admins()
    if admins:
        return ResponseModels(admins, "ADMINS_FOUND_SUCCESSFULLY")
    else:
        return ErrorResponseModel("Failed to find admins", "ADMINS_NOT_FOUND")
# Admin Update Admin
@router.put("/update_admin/{admin_id}", response_description="Update admin ")
async def update_admin(admin_id: str, admin:AdminSchema = Body(...)):
    admin = {k: v for k, v in admin.dict().items() if v is not None}
    if len(admin) >= 1:
        update_admin_data = await admin_controller.update_admin(admin_id, admin)
        # print(f"update_admin_data",update_admin_data)
        if update_admin_data:
            return ResponseUpdateTeacher("Admin updated successfully by admin:{0}".format(admin_id), "ADMIN_UPDATED_SUCCESSFULLY")
        else:
            return ErrorResponseModel(
                error="Failed to update admin {0}".format(admin_id),
                code="ADMIN_UPDATE_FAILED",
                message="Unable to update admin data. Please check the input and try again.")
# get admin by id
@router.get("/get_admin_id/{admin_id}", response_description="Get one admin")
async def get_admin_id(admin_id: str):
    admin = await admin_controller.get_admin_id(admin_id)
    if admin:
        return ResponseUpdateTeacher(admin, "ADMIN_FOUND_SUCCESSFULLY")
    else:
        return ErrorResponseModel("Failed to find admin{0}".format(admin_id),404, "ADMIN_NOT_FOUND")