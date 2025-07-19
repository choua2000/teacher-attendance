def attendance_helper(attendance_data):
    return {
        "id": str(attendance_data["_id"]),
        "teacher_id": attendance_data["teacher_id"],
        "teacher_name": attendance_data["teacher_name"],
        "classroom_id": attendance_data["classroom_id"],
        "classroom": attendance_data.get("class_room", {}),
        "confidence": attendance_data["confidence"],    
        "teacher_date": attendance_data["teacher_date"],
        "time": attendance_data["time"]
    }
def join_attendance_with_teacher(attendance, teacher, class_room):
    return {
        "teacher": {
            "name":teacher["name"],
            "first_name": teacher["first_name"],
            "last_name": teacher["last_name"],
            "email": teacher["email"],
            "age": teacher["age"],
            "phone": teacher["phone"],
            "position": teacher["position"]
        },
        "class_room":{
            "title": class_room["title"],
            "class_name": class_room["class_name"],
            "class_hour": class_room["class_hour"],
            "class_time": class_room.get("class_time", ""),
        },
        "teacher_date": attendance["teacher_date"],
        "confidence": attendance["confidence"],
        "time": attendance["time"]
    }
