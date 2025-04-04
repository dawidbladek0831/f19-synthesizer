from fastapi import FastAPI

from app.synthesizer import synthesizer_router

app = FastAPI()

app.include_router(
    synthesizer_router.router,
    prefix="/synthesizer",
    tags=["synthesizer"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}