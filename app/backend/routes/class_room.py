from fastapi import APIRouter, Body,Depends
from app.backend.helper.index import verify_jwt_token_and_role, ResponseUpdateClassRoom, ErrorResponseModel
from fastapi.encoders import jsonable_encoder
from app.backend.models.class_room import ClassRoomSchema,ClassRoomUpdateSchema
from app.backend.controllers.class_room import class_room_controller


router = APIRouter()

@router.post("/create_class_room", response_description="Create Class Room")
async def create_class_room(class_room: ClassRoomSchema = Body(...)):
    class_room_data = jsonable_encoder(class_room)
    
    result = await class_room_controller.create_class_room(class_room_data)
    return {
        "class_room": result["class_room"],
        "message": result["message"]
    }

@router.put("/update_class_room/{class_room_id}", response_description="Update Class Room")
async def update_class_room(
    class_room_id: str,
    class_room: ClassRoomUpdateSchema = Body(...)
    # payload: dict = Depends(verify_jwt_token_and_role)
):
    class_room_data = jsonable_encoder(class_room)
    success = await class_room_controller.update_class_room(class_room_id, class_room_data)

    if success:
        return ResponseUpdateClassRoom(f"Class Room updated successfully by admin: {class_room_id}", "CLASS_ROOM_UPDATED_SUCCESSFULLY")
    else:
        return ErrorResponseModel(
            error=f"Failed to update class room: {class_room_id}",
            code="CLASS_ROOM_UPDATE_FAILED",
            message="Unable to update classroom.",
            data=None
        )
# get all class rooms
@router.get("/get_all_class_rooms", response_description="Get all class rooms")
async def get_all_class_rooms():
    class_rooms = await class_room_controller.get_all_class_rooms()
    return {
        "data": class_rooms,
        "message": "CLASS_ROOMS_FOUND_SUCCESSFULLY"
    }
# get class room by id
@router.get("/get_class_room_by_id/{class_room_id}", response_description="Get one class room")
async def get_class_room_by_id(class_room_id: str):
    class_room = await class_room_controller.get_class_room_by_id(class_room_id)
    return {
        "data": class_room,
        "message": "CLASS_ROOM_FOUND_SUCCESSFULLY"

    }

# delete class room
@router.delete("/delete_class_room/{class_room_id}", response_description="Delete one class room")
async def delete_class_room(class_room_id: str):
    success = await class_room_controller.delete_class_room(class_room_id)
    if success:
        return ResponseUpdateClassRoom(f"Class Room deleted successfully by admin: {class_room_id}", "CLASS_ROOM_DELETED_SUCCESSFULLY")
    else:
        return ErrorResponseModel(f"Failed to delete class room: {class_room_id}", "CLASS_ROOM_DELETE_FAILED")