

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Union
import time
from datetime import datetime

from app.routers.auth import router as auth_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)

