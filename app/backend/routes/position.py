from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from app.backend.models.position import PositionSchema
from app.backend.controllers.position import position_controller
from app.backend.helper.index import ResponseModels, ErrorResponseModel
router = APIRouter()


@router.post("/create_position", response_description="Create a new position")
async def create_position(position: PositionSchema = Body(...)):
    if not position:
        return ErrorResponseModel("Failed to create position", 400, "POSITION_CREATION_FAILED")
    position_data = jsonable_encoder(position)
    result = await position_controller.create_position(position_data)
    if "message" in result:
        return ResponseModels(result["position"], result["message"])
    else:
        return ErrorResponseModel("Failed to create position", 400, "POSITION_CREATION_FAILED")
    
@router.get("/get_all_positions", response_description="Get all positions")
async def get_all_positions():
    positions = await position_controller.get_all_positions()
    if positions:
        return ResponseModels(positions, "POSITIONS_FOUND_SUCCESSFULLY")
    else:
        return ErrorResponseModel("Failed to find positions", 404, "POSITIONS_NOT_FOUND")