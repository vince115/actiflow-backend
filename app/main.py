# app/main.py
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="ActiFlow Backend",
    version="1.0.0"
)

# 掛上 API 分組
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "ActiFlow API is running!"}
