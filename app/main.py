import asyncio
from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.synthesizer import synthesizer_router

from app.logging_config import configure_logging

configure_logging()

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    synthesizer_router.router,
    prefix="/synthesizer",
    tags=["synthesizer"],
)

@app.get("/")
async def root(
    index: Annotated[str | None, Query()]
):
    print(f"root - start: {index}")
    await asyncio.sleep(1) 
    print(f"root - end: {index}")
    return {"message": "Hello World"}