from fastapi import FastAPI
from app.backend.routes.index import router as ApiRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Teacher Auth API")

origins = [
    "http://192.168.43.210:3000",  # Nuxt app
    # "http://192.168.68.218:3000",
    "http://localhost:8000", # FastAPI app
    "http://127.0.0.1:8000",    # FastAPI app
    "http://localhost:3000",  # Nuxt app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE",],
    allow_headers=["*"],
)

app.include_router(ApiRouter, prefix="/api", tags=["api"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
