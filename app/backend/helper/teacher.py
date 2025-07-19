import numpy as np
import pandas as pd
# import torch
# def teacher_helper(teacher) -> dict:
#     return {
#         "id": str(teacher["_id"]),
#         # "name": teacher["name"],
#         "first_name": teacher["first_name"],
#         "last_name":teacher["last_name"],
#         "age": teacher["age"],
#         "email": teacher["email"],  
#         "position": teacher["position"],
#         "phone": teacher["phone"]
#     }
def teacher_helper(teacher) -> dict:
    return {
        "id": str(teacher.get("_id", "")),
        "classroom_id": teacher.get("classroom_id", ""),
        "name": teacher.get("name", "No Name"),
        "first_name": teacher.get("first_name", ""),
        "last_name": teacher.get("last_name", ""),
        "age": teacher.get("age", 0),
        "email": teacher.get("email", ""),
        "position": teacher.get("position", ""),
        "phone": teacher.get("phone", "")
    }
def join_classroom_with_teacher(class_room, teacher):
    return {
        # "class_room": {
        #     "title": class_room["title"],
        #     "class_name": class_room["class_name"],
        #     "class_hour": class_room["class_hour"],
        #     "time": class_room.get("time", "")
        # },
        "teacher": {
            "name":teacher["name"],
            "first_name": teacher["first_name"],
            "last_name": teacher["last_name"],
            "email": teacher["email"],
            "age": teacher["age"],
            "phone": teacher["phone"],
            "position": teacher["position"]
        },
    }
