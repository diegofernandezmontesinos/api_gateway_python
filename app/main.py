from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI()
app.include_router(router)

# 🚀 Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ acepta cualquier origen en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # permite GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # permite todos los headers, incluido X-API-KEY
)
