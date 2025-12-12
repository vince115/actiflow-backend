# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.api.utils.debug import router as debug_router

app = FastAPI(
    title="ActiFlow Backend",
    version="1.0.0"
)

# ⭐ CORS 設定（前端 Next.js 必須要這段）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # ⭐ 必須加，不然 OPTIONS 會 405
    allow_headers=["*"],   # ⭐ 讓 Authorization / JSON 等 headers 都可用
)


# 掛上 API 分組
app.include_router(api_router)
app.include_router(debug_router)

@app.get("/")
def root():
    return {"message": "ActiFlow API is running!"}
