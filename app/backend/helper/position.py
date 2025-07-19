def position_helper(position) -> dict:
    return {
        "id": str(position["_id"]),
        "room_password": position.get["room_id"],
        "room_name": position.get["room_name"],
        "hour": position.get["hour"]
    }