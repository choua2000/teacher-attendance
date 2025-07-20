from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Form
import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from app.backend.models.attendance import AttendanceSchema
from app.backend.controllers.attendance import attendance_controller
from app.backend.controllers.class_room import class_room_controller
from app.backend.controllers.teacher import teacher_controller
from app.backend.helper.index import ResponseModels, ErrorResponseModel
from app.backend.helper.attendance import attendance_helper

import numpy as np
from PIL import Image
import io
import tensorflow as tf

router = APIRouter()

# ✅ Load your model globally to avoid reloading every time
# model = tf.keras.models.load_model("../models/model_facce/best_mobilenet_model.h5")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/model_facce/best_model_21th.h5")
# model = tf.keras.models.load_model(MODEL_PATH,custom_objects={'TrueDivide': tf.keras.layers.Lambda(lambda x: x)} )
model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'TrueDivide': tf.math.truediv})
class_names = [
    "AJ Amone",
    "AJ Bouasod",
    "AJ Bounmee",
    "AJ Chidnavan",
    "AJ Khamkon",
    "AJ Khamla",
    "AJ Latsamee",
    "AJ Muenphin",
    "AJ Ngaviset",
    "AJ Oladee",
    "AJ Ouksavan",
    "AJ Phonsouda",
    "AJ Phouthon",
    "AJ Siarmphone",
    "AJ Sommany",
    "AJ Sommid",
    "AJ Soupkasert",
    "AJ Soulid",
    "AJ Soupaivi",
    "AJ Thongsing",
    "AJ Vilaisak"
]  

def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((224, 224))  # Adjust based on model input
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0) / 255.0
    return img_array

# @router.post("/predict_attendance", response_description="Predict and save teacher attendance")
# async def predict_attendance(
#     file: UploadFile = File(...),
#     ## classroom data
#     classroom_id: str = Form(...),
#     ):
#     try:
#         contents = await file.read()
#         img_array = preprocess_image(contents)

#         prediction = model.predict(img_array)
#         predicted_class_index = np.argmax(prediction)
#         predicted_name = class_names[predicted_class_index]
#         confidence = float(np.max(prediction))

#         threshold = 0.70
#         if confidence <= threshold:
#             return {
#                 "found": False,
#                 "name": "Unknown",
#                 "confidence": confidence * 100,
#                 "message": f"❌ ບໍ່ຮູ້ຈັກບຸກຄົນ (confidence {confidence*100:.2f}%)",
#                 "data": []
#             }

#         teacher = await teacher_controller.get_teacher_by_name(predicted_name)
#         if not teacher:
#             return {
#                 "found": False,
#                 "name": predicted_name,
#                 "confidence": confidence * 100,
#                 "message": "❌ ບໍ່ພົບຜູ້ນີ້ໃນລະບົບ",
#                 "data": []
#             }

#         today = datetime.today().strftime('%Y-%m-%d')
#         note = "ປັດຈບັນ"
#         attendance_data = AttendanceSchema(
#             teacher_id=str(teacher["_id"]),
#             ## classroom data
#             classroom_id=str(classroom_id), #classroom_id,
#             teacher_name=teacher["name"],
#             teacher_date={"day": today, "note": note},
#             confidence=confidence,
#             time=datetime.now().strftime('%H:%M:%S')
#         )
#         attendance_json = jsonable_encoder(attendance_data)
#         result = await attendance_controller.add_attendance(attendance_json)

#         return {
#             "found": True,
#             "name": predicted_name,
#             "confidence": confidence * 100,
#             "message": f"✅ ການສະແກນສຳເລັດ: {predicted_name} ({confidence*100:.2f}%)",
#             "data": result["attendance"]
#         }

#     except HTTPException as e:
#         return {
#             "found": False,
#             "name": "Unknown",
#             "confidence": 0,
#             "message": str(e.detail),
#             "data": []
#         }
#     except Exception as e:
#         return {
#             "found": False,
#             "name": "Unknown",
#             "confidence": 0,
#             "message": str(e),
#             "data": []
#         }




@router.post("/predict_attendance", response_description="Predict and save teacher attendance")
async def predict_attendance(
    file: UploadFile = File(...),
    classroom_id: str = Form(...)
):
    try:
        contents = await file.read()
        img_array = preprocess_image(contents)

        prediction = model.predict(img_array)
        predicted_class_index = np.argmax(prediction)
        predicted_name = class_names[predicted_class_index]
        confidence = float(np.max(prediction))
        print(f"🎯 Predicted class index: {predicted_class_index}")
        print(f"🎯 Predicted name: {predicted_name}")
        print(f"🎯 Confidence: {confidence*100:.2f}%")
        print(f"🔍 Searching teacher by name: {predicted_name}")

        threshold = 0.70
        if confidence <= threshold:
            return {
                "found": False,
                "name": "Unknown",
                "confidence": confidence * 100,
                "message": f"❌ ບໍ່ຮູ້ຈັກບຸກຄົນ (confidence {confidence*100:.2f}%)",
                "data": []
            }

        teacher = await teacher_controller.get_teacher_by_name(predicted_name)
        print(f"🔍 Teacher found: {teacher}")
        if not teacher:
            return {
                "found": False,
                "name": predicted_name,
                "confidence": confidence * 100,
                "message": "❌ ບໍ່ພົບຜູ້ນີ້ໃນລະບົ",
                "data": []
            }

        # ─── ดึงข้อมูลห้อง ───
        classroom = await class_room_controller.get_class_room_by_id(classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="CLASS_ROOM_NOT_FOUND")

        # หาเวลาเริ่มประชุม
        meeting_start_dt = None
        if "class_time" in classroom:  # ISO เช่น 2025-07-30T17:00:00.000Z
            raw_time = classroom["class_time"]
            # แปลง (รองรับมี 'Z')
            if raw_time.endswith("Z"):
                raw_time = raw_time.replace("Z", "+00:00")
            meeting_start_dt = datetime.fromisoformat(raw_time)
        elif "class_hour" in classroom:
            # สมมุติ class_hour = "14:00-15:30"
            today_str = datetime.today().strftime("%Y-%m-%d")
            start_part = classroom["class_hour"].split("-")[0].strip()
            meeting_start_dt = datetime.strptime(f"{today_str} {start_part}", "%Y-%m-%d %H:%M")
        else:
            # fallback: ใช้เวลาปัจจุบันเป็น meeting start
            meeting_start_dt = datetime.now()

        scan_dt = datetime.now()
        late_delta = scan_dt - meeting_start_dt
        late_minutes = int(late_delta.total_seconds() // 60)

        if late_minutes <= 10:
            status = "มา"
        else:
            status = "มาช้าแล้ว"

        today = datetime.today().strftime('%Y-%m-%d')
        note = "ປັດຈຸບັນ"

        attendance_doc = AttendanceSchema(
            teacher_id=str(teacher["_id"]),
            classroom_id=classroom_id,
            name=teacher["name"],
            teacher_date={"day": today, "note": note},
            confidence=confidence,
            time=scan_dt.strftime('%H:%M:%S'),
            status=status,
            meeting_start=meeting_start_dt.isoformat(),
            scan_time=scan_dt.isoformat(),
            late_minutes=max(late_minutes, 0)
        )

        attendance_json = jsonable_encoder(attendance_doc)
        result = await attendance_controller.add_attendance(attendance_json)

        return {
            "found": True,
            "name": predicted_name,
            "confidence": confidence * 100,
            "status": status,
            "late_minutes": max(late_minutes, 0),
            "message": f"✅ {status}: {predicted_name} ({confidence*100:.2f}%)",
            "data": result["attendance"]
        }

    except HTTPException as e:
        return {
            "found": False,
            "name": "Unknown",
            "confidence": 0,
            "message": str(e.detail),
            "data": []
        }
    except Exception as e:
        return {
            "found": False,
            "name": "Unknown",
            "confidence": 0,
            "message": str(e),
            "data": []
        }


#########  new code ########


# @router.post("/predict_attendance", response_description="Predict and save teacher attendance")
# async def predict_attendance(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         img_array = preprocess_image(contents)

#         prediction = model.predict(img_array)
#         predicted_class_index = np.argmax(prediction)
#         predicted_name = class_names[predicted_class_index]

#         confidence = float(np.max(prediction))

#         # ตรวจสอบข้อมูลอาจารย์
#         teacher = await teacher_controller.get_teacher_by_name(predicted_name)
#         if not teacher:
#             raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")

#         # สร้างข้อมูลบันทึกเวลา
#         today = datetime.today().strftime('%Y-%m-%d')
#         attendance_data = AttendanceSchema(
#             teacher_id=str(teacher["_id"]),
#             teacher_name=teacher["first_name"],
#             teacher_date={
#                 "day": today,
#                 "note": "Present"
#             },
#             confidence=confidence,
#             time=datetime.now().strftime('%H:%M:%S')
#         )
#         attendance_json = jsonable_encoder(attendance_data)
#         result = await attendance_controller.add_attendance(attendance_json)

#         return ResponseModels(result["attendance"], f"{predicted_name} ດ້ວຍຄວາມແມ່ນຍຳ {confidence*100:.2f}%")

#     except HTTPException as e:
#         return ErrorResponseModel(e.detail, e.status_code, "ATTENDANCE_FAILED")
#     except Exception as e:
#         return ErrorResponseModel(str(e), 500, "PREDICTION_ERROR")

############## route predict_attendance ##############

# @router.post("/predict_attendance", response_description="Predict and save teacher attendance")
# async def predict_attendance(
#     file: UploadFile = File(...)):
#     # classroom_id: str = Form(...)) :
#     try:
#         contents = await file.read()
#         img_array = preprocess_image(contents)

#         prediction = model.predict(img_array)
#         predicted_class_index = np.argmax(prediction)
#         predicted_name = class_names[predicted_class_index]
#         confidence = float(np.max(prediction))

#         # กำหนด threshold
#         threshold = 0.70
#         if confidence <= threshold:
#             return ErrorResponseModel("Unknown face", 400, f"ບໍ່ຮູ້ຈັກບຸກຄົນ (confidence {confidence*100:.2f}%)")

#         # ตรวจสอบข้อมูลอาจารย์
#         teacher = await teacher_controller.get_teacher_by_name(predicted_name)
#         if not teacher:
#             raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")
#         # get classroom by id
#         # classroom = await class_room_controller.get_class_room_by_id(classroom_id)
#         # if not classroom:
#         #     raise HTTPException(status_code=404, detail="CLASS_ROOM_NOT_FOUND")
#         # สร้างข้อมูลบันทึกเวลา
#         today = datetime.today().strftime('%Y-%m-%d')
#         note = "ປັດຈບັນ"
#         attendance_data = AttendanceSchema(
#             teacher_id=str(teacher["_id"]),
#             # classroom_id=str(classroom["id"]),
#             teacher_name=teacher["name"],

#             teacher_date={
#                 "day": today,
#                 "note": note
#             },
#             confidence=confidence,
#             time=datetime.now().strftime('%H:%M:%S')
#         )
#         attendance_json = jsonable_encoder(attendance_data)
#         print(f"attendance_json class: {attendance_json}")
#         result = await attendance_controller.add_attendance(attendance_json)
#         print(f"result class: {result}")
#         return ResponseModels(200,
#             result["attendance"],
#             f"✅ ການສະແກນສຳເລັດ: {predicted_name} ດ້ວຍຄວາມແມ່ນຍຳ {confidence*100:.2f}%"
#         )
#     except HTTPException as e:
#         return ErrorResponseModel(e.detail, e.status_code, "ອຈ ມີຢູ່ໃນລະບົບແລ້ວ",[])
#     except Exception as e:
#         return ErrorResponseModel(str(e), 500, "PREDICTION_ERROR",[])
    