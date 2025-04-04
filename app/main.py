import asyncio
from typing import Annotated
from fastapi import FastAPI, Query

from app.synthesizer import synthesizer_router

app = FastAPI()

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