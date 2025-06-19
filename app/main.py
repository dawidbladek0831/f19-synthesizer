import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.synthesizer import synthesizer_router

from app.logging_config import configure_logging

configure_logging()

app = FastAPI()

origins = [
    "https://f19.dev.dawidbladek0831.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    synthesizer_router.router,
    prefix="/synthesizer",
    tags=["synthesizer"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}