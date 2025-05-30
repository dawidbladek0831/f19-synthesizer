import pytest
import asyncio
import httpx
from fastapi.testclient import TestClient

from app.main import app  as fastapi

client = httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi), base_url="http://testserver", timeout=1200.0)
client2 = httpx.AsyncClient(base_url="http://localhost:8000", timeout=1200.0)
active_client = client2

@pytest.mark.asyncio
async def test_synthesizer_concurrent_requests():
    text  =  "The time module has a function sleep() that you can use to suspend execution of the calling thread for however many seconds you specify."
    async with active_client:
        tasks = [ active_client.get("/synthesizer", params={"model_id": "speecht5", "speaker_id":7306, "language": "ENG", "text": text}) 
                 for i in range(10)]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "audio/wav"
        assert response.headers["Content-Disposition"] == "attachment; filename=output.wav"
        assert len(response.content) > 0