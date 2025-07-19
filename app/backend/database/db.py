from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://chouavang:chouavang@cluster0.egqgukp.mongodb.net/attendance_tracker?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL)
# db = client["teacher_db"]
db = client["attendance_db"]
teachers_collection = db["teachers"]
admins_collection = db["admins"]
class_rooms_collection = db["class_rooms"]
attendance_collection = db["attendance"]
meeting_collection = db["meeting"]
positions_collection = db["positions"]
report_collection = db["report"]