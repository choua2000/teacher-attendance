from fastapi import HTTPException, status
from app.backend.database.db import admins_collection
from app.backend.helper.admin import admin_helper
from datetime import datetime, timedelta
import uuid, bcrypt
import jwt 
from bson import ObjectId
SECRET_KEY = "choua12345"

class AdminController:
    def __init__(self, collection):
        self.collection = collection

    async def admin_register(self, admin_data: dict) -> dict:
        existing = await self.collection.find_one({"email": admin_data["email"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="USER_ALREADY_EXISTS"
            )

        # Hash password
        password = admin_data.get("password")
        if not password:
            raise HTTPException(status_code=400, detail="Password is required")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_data["password"] = hashed
        # admin_data["_id"] = str(uuid.uuid4())

        await self.collection.insert_one(admin_data)
        new_admin = await self.collection.find_one({"email": admin_data["email"]})

        return {
            "message": "ADMIN_REGISTERED_SUCCESSFULLY",
            "admin": admin_helper(new_admin)
        }

    # Admin login
    async def admin_login(self, admin_data: dict) -> dict:
        email = admin_data.get("email")
        password = admin_data.get("password")

        admin = await self.collection.find_one({"email": email})
        if not admin:
            raise HTTPException(status_code=404, detail="USER_NOT_FOUND")

        if bcrypt.checkpw(password.encode('utf-8'), admin["password"].encode('utf-8')):

         token = self.generate_token(str(admin["_id"]), admin["role"])
         if admin["role"] == "admin":
            return token, admin_helper(admin), "ADMIN_LOGIN_SUCCESSFULLY"
        else:
            raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
        return token, admin_helper(admin), "ADMIN_LOGIN_SUCCESSFULLY"
    # Generate JWT token
    def generate_token(self, admin_id: str, role: str) -> str:
        payload = {
            "_id": str(admin_id),
            "role": role,
            "exp": datetime.utcnow() + timedelta(days=1) # Token valid for 1 day
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    
    # get admin all
    async def get_all_admins(self) -> list:
        admins = []
        async for admin in self.collection.find():
            admins.append(admin_helper(admin))
        return admins
    # update admin
    async def update_admin(self, admin_id: str, admin_data: dict):
        admin_data = {k: v for k, v in admin_data.items() if v is not None}
        if len(admin_data) >= 1:
            update_admin = await self.collection.update_one({"_id": ObjectId(admin_id)}, {"$set": admin_data})
            if update_admin.modified_count == 1:
                updated_admin = await self.collection.find_one({"_id": ObjectId(admin_id)})
                return admin_helper(updated_admin)
        return None
    # get admin by id
    async def get_admin_id(self, admin_id: str) -> dict:
        admin = await self.collection.find_one({"_id": ObjectId(admin_id)})
        if admin:
            return admin_helper(admin)
        return None
admin_controller = AdminController(admins_collection)