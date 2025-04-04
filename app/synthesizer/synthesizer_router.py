from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse  # Import StreamingResponse
from pydantic import BaseModel

from app.synthesizer import synthesizer

router = APIRouter()

@router.get("/")
async def syntesizer(
    model_id: Annotated[str | None, Query()],
    language: Annotated[synthesizer.Language | None, Query()],
    text: Annotated[str | None, Query()],
):
    model = synthesizer.get_model(model_id, language)
    file = model.synthesize(text)

    return StreamingResponse(
        file,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=output.wav"}
    )