from typing import Annotated
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse 
from asyncio import to_thread

from app.synthesizer.text_to_speech_models import Language
from app.synthesizer.text_to_speech_models_manager import get_text_to_speech_models_manager

router = APIRouter()


@router.get(path="")
async def syntesizer(
    model_id: Annotated[str | None, Query()],
    speaker_id: Annotated[int | None, Query()],
    language: Annotated[Language | None, Query()],
    text: Annotated[str | None, Query()],
):
    print(f"model - start: {text}")
    model = get_text_to_speech_models_manager().get_model(model_id, language)
    file = await to_thread(model.synthesize, text, speaker_id) 
    print(f"model - end: {text}")

    return StreamingResponse(
        file,
        media_type="audio/wav",
        headers={"Content-Disposition": "attachment; filename=output.wav"}
    )