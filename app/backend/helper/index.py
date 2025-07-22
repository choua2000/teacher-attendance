from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()
from jwt import PyJWTError
from app.backend.controllers.admin import SECRET_KEY
import jwt
def ResponseRegister(teacher,  message):
    return {
        "code": 200,
        "message": message,
        "teacher": teacher,
        # "token": token
    }

def ResponseLogin(admin, token, message):
    return {
        "data":{
            "admin": admin,
            "token": token
        },
        "code": 200,
        "message": message,
    }
def ResponseUpdateTeacher(teacher, message):
    return {
        "code": 201,
        "message": message,
        "teacher": teacher
    }
def ErrorResponseModel(error: str, code: int, message: str,data:str ):
    if data is None:
        data = []
    return {
        "code": code,
        "error": error,
        "message": message,
        "data": data # ✅ ไม่มีข้อมูลก็ต้องส่ง list ว่าง
    }

def ResponseDeleteTeacher( message):
    return {
        "code": 200,
        "message": message,

    }


def ResponseUpdateClassRoom(message, class_room, ):
    return {
        "code": 200,
        "message": message,
        "class_room": class_room
    }
def ResponseModels(data, message):
    return {
        "code": 200,
        "massage": message,
        "data": data,
    }
def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")
    
def verify_jwt_token_and_role(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["role"] == "admin":
            return payload
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")
