# # report 
# def report_helper(report) -> dict:
#     return {
#         "id": str(report["_id"]),
#         "attendance_id": report["attendance_id"],
#         "title": report["title"],
#         "class_name": report["class_name"],
#         "hour": report["hour"],
#         "time": report("time", ""),
#     }
# def join_report_with_attendance(report, attendance):
#     return {
#         "id": str(report["_id"]),
#         "attendance_id": attendance["attendance_id"],
#         "class_name": report["class_name"],
#         "hour": report["hour"],
#         "time": report("time", ""),
#         "title": report["title"],
        
#     }
from bson import ObjectId
from fastapi import HTTPException # You must define these

def report_helper(report) -> dict:
    return {
        "id": str(report["_id"]),
        "attendance_id": report["attendance_id"],
        "title": report["title"],
        "class_name": report["class_name"],
        "hour": report["hour"],
        "time": report.get("time", ""),
    }

def attendance_helper(attendance_data) -> dict:
    return {
        "id": str(attendance_data["_id"]),
        "teacher_id": attendance_data["teacher_id"],
        "confidence": attendance_data["confidence"],
        "teacher_date": attendance_data["teacher_date"],
        "time": attendance_data["time"]
    }

def join_report_with_attendance(report, attendance):
    return {
        "id": str(report["_id"]),
        "attendance_id": report["attendance_id"],
        "title": report["title"],
        "class_name": report["class_name"],
        "hour": report["hour"],
        "time": report.get("time", ""),
        "attendance": attendance_helper(attendance)
    }


