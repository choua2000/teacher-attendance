from app.backend.database.db import report_collection, attendance_collection
from fastapi import HTTPException, status
from app.backend.helper.report import report_helper, join_report_with_attendance, attendance_helper
from app.backend.models.report import ReportSchema, AttendanceSchema
from bson import ObjectId

class ReportController:
    def __init__(self, collection):
        self.collection = collection
    # add new report record
    async def add_report(self, report_data: ReportSchema):
        existing = await self.collection.find_one({"attendance_id": report_data["attendance_id"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="REPORT_ALREADY_EXISTS"
            )

        await self.collection.insert_one(report_data)
        new_report = await self.collection.find_one({"attendance_id": report_data["attendance_id"]})

        return {
            "message": "REPORT_ADDED_SUCCESSFULLY",
            "report": join_report_with_attendance(new_report)
}


        