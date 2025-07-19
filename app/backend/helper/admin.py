def admin_helper(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "fullname": admin["fullname"],
        "email": admin["email"],
        "password": admin["password"],  
        "age": admin["age"],
        "phone": admin["phone"],
        "role": admin["role"]
    } 