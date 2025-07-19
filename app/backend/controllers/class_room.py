from fastapi import status,HTTPException
from app.backend.database.db import class_rooms_collection
from app.backend.helper.class_room import class_room_helper
from bson import ObjectId
from datetime import datetime, timedelta


class ClassRoomController:
    def __init__(self, collection):
        self.collection = collection
     # ADD NEW CLASS_ROOM
    async def create_class_room(self, class_room_data: dict) -> dict:
        existing = await self.collection.find_one({"class_name": class_room_data["class_name"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CLASS_ROOM_ALREADY_EXISTS"
            )

        await self.collection.insert_one(class_room_data)
        new_class_room = await self.collection.find_one({"class_name": class_room_data["class_name"]})
        return {
            "message": "CLASS_ROOM_CREATED_SUCCESSFULLY",
            "class_room": class_room_helper(new_class_room)
        }

    async def update_class_room(self, class_room_id: str, update_data: dict) -> bool:
         if len(update_data) < 1:
            return False

         existing = await self.collection.find_one({"_id": ObjectId(class_room_id)})
         if not existing:
            raise HTTPException(
                status_code=404,
                detail="CLASS_ROOM_NOT_FOUND"
            )

         update_result = await self.collection.update_one(
            {"_id": ObjectId(class_room_id)},
            {"$set": update_data}
        )
         return update_result.modified_count > 0
   # get all class rooms
    async def get_all_class_rooms(self):
        class_rooms = []
        async for class_room in self.collection.find():
            class_rooms.append(class_room_helper(class_room))
        return class_rooms
    # get class room by id
    async def get_class_room_by_id(self, class_room_id: str):
        if not ObjectId.is_valid(class_room_id):
            raise HTTPException(status_code=404, detail="CLASS_ROOM_NOT_FOUND")
        class_room = await self.collection.find_one({"_id": ObjectId(class_room_id)})
        if class_room:
            return class_room_helper(class_room)
        raise HTTPException(status_code=404, detail="CLASS_ROOM_NOT_FOUND")
    
    # delete class room by id
    async def delete_class_room(self, class_room_id: str):
        if not ObjectId.is_valid(class_room_id):
            raise HTTPException(status_code=404, detail="CLASS_ROOM_NOT_FOUND")
        result = await self.collection.find_one({"_id":ObjectId(class_room_id) })
        if result:
            deleted_class_room = await self.collection.delete_one({"_id": ObjectId(class_room_id)})
            if deleted_class_room.deleted_count > 0:
                return True
            return False
    # get class room by id
    
class_room_controller = ClassRoomController(class_rooms_collection)

