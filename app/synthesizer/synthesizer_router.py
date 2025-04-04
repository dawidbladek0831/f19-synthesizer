from typing import Annotated
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse 
from asyncio import to_thread

from app.synthesizer import synthesizer

router = APIRouter()

@router.get(path="")
async def syntesizer(
    model_id: Annotated[str | None, Query()],
    speaker_id: Annotated[int | None, Query()],
    language: Annotated[synthesizer.Language | None, Query()],
    text: Annotated[str | None, Query()],
):
    print(f"model - start: {text}")
    model = synthesizer.get_model(model_id, language)
    file = await to_thread(model.synthesize, text, speaker_id) 
    print(f"model - end: {text}")

    return StreamingResponse(
        file,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=output.wav"}
    )