from fastapi import APIRouter, Body ,HTTPException
from fastapi.encoders import jsonable_encoder
from app.backend.models.attendance import AttendanceSchema,AttendanceListResponse
from app.backend.controllers.attendance import attendance_controller
from app.backend.helper.attendance import attendance_helper
from app.backend.database.db import attendance_collection, teachers_collection
from app.backend.helper.index import ResponseModels, ErrorResponseModel
from bson import ObjectId
router = APIRouter()
# retrieve attendance 
# load class_names.txt

@router.get("/get_all_attendance", response_description="Get all attendance records")
async def get_all_attendance(time: str, start_date: str = None, end_date: str = None):
    try:
        attendance_records = await attendance_controller.retrieve_attendance(time, start_date, end_date)
        if attendance_records:
            return ResponseModels(attendance_records, "ATTENDANCE_FOUND_SUCCESSFULLY")
        else:
            return ErrorResponseModel("No attendance records found", 404, "ATTENDANCE_NOT_FOUND")
    except Exception as e:
        return ErrorResponseModel(str(e), 500, "INTERNAL_SERVER_ERROR")
    
# Add new attendance record
@router.post("/add_attendance", response_description="Add new attendance record")
async def add_attendance(attendance: AttendanceSchema = Body(...)):
    attendance_data = jsonable_encoder(attendance)
    try:
        result = await attendance_controller.add_attendance(attendance_data)
        return ResponseModels(result["attendance"], result["message"])
    except HTTPException as e:
        return ErrorResponseModel(e.detail, e.status_code, "ATTENDANCE_CREATION_FAILED")
    except Exception as e:
        return ErrorResponseModel(str(e), 500, "INTERNAL_SERVER_ERROR")
    
# Get all attendance records
@router.get("/get_all_attendance_records", response_description="Get all attendance records")
async def get_all_attendance_records():
    try:
        attendance_records = await attendance_controller.get_all_attendance()
        if attendance_records:
            return ResponseModels(attendance_records, "ATTENDANCE_RECORDS_FOUND_SUCCESSFULLY")
        else:
            return ErrorResponseModel("No attendance records found", "ATTENDANCE_RECORDS_NOT_FOUND")
    except Exception as e:
        return ErrorResponseModel(str(e), 500, "INTERNAL_SERVER_ERROR")


# Get attendance by teacher
@router.get("/attendance", response_model=AttendanceListResponse, response_description="Get all attendance records")
async def get_attendance_with_teacher():
    try:
        attendances = await attendance_controller.get_attendance_with_teacher()
        if attendances:
            return {
                "code": 200,
                "message": "ATTENDANCE_WITH_TEACHER_FOUND_SUCCESSFULLY",
                "data": attendances
            }
        else:
            return ErrorResponseModel(error="No attendance records found",code= 404, message="ATTENDANCE_WITH_TEACHER_NOT_FOUND")
    except Exception as e:
        return ErrorResponseModel(str(e), 500, "INTERNAL_SERVER_ERROR",data=[ ])
    
# delete attendance
@router.delete("/delete_attendance/{attendance_id}", response_description="Delete attendance")
async def delete_attendance(attendance_id: str):
    try:
        attendance = await attendance_controller.delete_attendance(attendance_id)

        if attendance is None:
            raise HTTPException(status_code=404, detail="ATTENDANCE_NOT_FOUND")
        attendance["_id"] = str(attendance["_id"])
        encoded_attendance = jsonable_encoder(attendance)
        return ResponseModels(encoded_attendance, "ATTENDANCE_DELETED_SUCCESSFULLY")

    except HTTPException as e:
        return ErrorResponseModel(e.detail, e.status_code, "ATTENDANCE_DELETE_FAILED")
    except Exception as e:
        return ErrorResponseModel(str(e), 500, "INTERNAL_SERVER_ERROR")
   

    

