from app.backend.database.db import positions_collection
from app.backend.helper.position import position_helper
from fastapi import status, HTTPException
from bson import ObjectId
from app.backend.models.position import PositionSchema

class PositionController:
    def __init__(self, collection):
        self.collection = collection
    async def create_position(self, position_data: PositionSchema) -> dict:
        existing = await self.collection.find_one({"room_password": position_data["room_password"]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="POSITION_ALREADY_EXISTS"
            )

        await self.collection.insert_one(position_data)
        new_position = await self.collection.find_one({"room_password": position_data["room_password"]})

        return {
            "message": "POSITION_CREATED_SUCCESSFULLY",
            "position": position_helper(new_position)
        }
    # get all positions
    async def get_all_positions(self) -> list:
        positions = await self.collection.find().to_list(length=None)
        return [position_helper(position) for position in positions]
    
position_controller = PositionController(positions_collection)