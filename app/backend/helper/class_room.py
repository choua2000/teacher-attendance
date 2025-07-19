# def class_room_helper(class_room) -> dict:
#     return {
#         "id": str(class_room["_id"]),
#         "title": class_room["title"],
#         "class_name": class_room["class_name"],
#         "class_hour": class_room["class_hour"],
#         "data": class_room["data"]
#     }

def class_room_helper(class_room) -> dict:
    return {
        "id": str(class_room["_id"]),
        "title": class_room["title"],
        "class_name": class_room["class_name"],
        "class_hour": class_room["class_hour"],
        "class_time": class_room.get("class_time", ""),
    }
