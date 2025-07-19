from fastapi import APIRouter,File, UploadFile, HTTPException, status
import shutil
from app.backend.routes.teacher import router as TeacherRouter
from app.backend.routes.admin import router as AdminRouter
from app.backend.routes.class_room import router as ClassRoomRouter
from app.backend.routes.position import router as PositionRouter
from app.backend.routes.attendance import router as AttendanceRouter
from app.backend.routes.meetingroom import router as MeetingRoomRouter
import os

# from app.backend.routes.camera import router as CameraRouter
# from app.backend.routes.traimodel import router as TrainModelRouter
router = APIRouter()

router.include_router(TeacherRouter, prefix="/teacher", tags=["teacher"])
router.include_router(AdminRouter, prefix="/admin", tags=["admin"])
router.include_router(ClassRoomRouter, prefix="/class_room", tags=["class_room"])
router.include_router(PositionRouter, prefix="/position", tags=["position"])
router.include_router(AttendanceRouter, prefix="/attendance", tags=["attendance"])
router.include_router(MeetingRoomRouter, prefix="/meeting_room", tags=["meeting_room"])
# router.include_router(CameraRouter, prefix="/camera", tags=["camera"])
# router.include_router(TrainModelRouter, prefix="/train_model", tags=["train_model"])

# # from fastapi import APIRouter, File, UploadFile, HTTPException, status
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from datetime import datetime
# from app.backend.models.attendance import AttendanceSchema
# from app.backend.controllers.attendance import attendance_controller
# from app.backend.controllers.teacher import teacher_controller
# from app.backend.helper.index import ResponseModels, ErrorResponseModel
# from app.backend.helper.attendance import attendance_helper

# import numpy as np
# from PIL import Image
# import io
# import tensorflow as tf

# router = APIRouter()

# # ✅ Load your model globally to avoid reloading every time
# # model = tf.keras.models.load_model("../models/model_facce/best_mobilenet_model.h5")
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "../models/model_facce/best_model_21th.h5")
# # model = tf.keras.models.load_model(MODEL_PATH,custom_objects={'TrueDivide': tf.keras.layers.Lambda(lambda x: x)} )
# model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'TrueDivide': tf.math.truediv})
# class_names = [
#     "AJ Amone",
#     "AJ Bouasod",
#     "AJ Bounmee",
#     "AJ Chidnavan",
#     "AJ Khamkon",
#     "AJ Khamla",
#     "AJ Latsamee",
#     "AJ Muenphin",
#     "AJ Ngaviset",
#     "AJ Oladee",
#     "AJ Ouksavan",
#     "AJ Phonsouda",
#     "AJ Phouthon",
#     "AJ Siarmphone",
#     "AJ Sommany",
#     "AJ Sommid",
#     "AJ Soupkasert",
#     "AJ Soulid",
#     "AJ Soupaivi",
#     "AJ Thongsing",
#     "AJ Vilaisak"
# ]  # <- 🛑 Add your 21 class names in order here: ['John', 'Mary', ...]

# def preprocess_image(image_bytes):
#     image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#     image = image.resize((224, 224))  # Adjust based on model input
#     img_array = tf.keras.preprocessing.image.img_to_array(image)
#     img_array = tf.expand_dims(img_array, 0) / 255.0
#     return img_array

# @router.post("/predict_attendance", response_description="Predict and save teacher attendance")
# async def predict_attendance(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         img_array = preprocess_image(contents)

#         prediction = model.predict(img_array)
#         predicted_class_index = np.argmax(prediction)
#         predicted_name = class_names[predicted_class_index]

#         print(f"Predicted class: {predicted_name}")
#         confidence = float(np.max(prediction))

#         # Check teacher in DB by name
#         teacher = await teacher_controller.get_teacher_by_name(predicted_name)
#         print(f"teacher class: {teacher}")

#         if not teacher:
#             raise HTTPException(status_code=404, detail="TEACHER_NOT_FOUND")

#         # Prepare attendance data
#         today = datetime.today().strftime('%Y-%m-%d')
#         attendance_data = AttendanceSchema(
#             teacher_id=str(teacher["_id"]),
#             teacher_name=teacher["first_name"],
#             #teacher_date is dict
#             teacher_date= {
#                 "day": today,
#                 "note": "Present"
#             },
#             confidence=confidence,
#             time=datetime.now().strftime('%H:%M:%S')
#         )
#         attendance_json = jsonable_encoder(attendance_data)
#         print(f"attendance_json class: {attendance_json}")

#         result = await attendance_controller.add_attendance(attendance_json)

#         return ResponseModels(result["attendance"], f"{predicted_name} marked present with {confidence*100:.2f}% confidence")

#     except HTTPException as e:
#         return ErrorResponseModel(e.detail, e.status_code, "ATTENDANCE_FAILED")
#     except Exception as e:
#         return ErrorResponseModel(str(e), 500, "PREDICTION_ERROR")
