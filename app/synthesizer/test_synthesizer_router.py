import pytest
import asyncio
import httpx
from fastapi.testclient import TestClient

from app.main import app as fastAPI

client = TestClient(fastAPI)

# @pytest.mark.asyncio
# async def test_synthesizer_concurrent_requests():
#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         tasks = [ client.get("/",params={"index":i}) for i in range(200)]
#         responses = await asyncio.gather(*tasks)

#     for response in responses:
#         assert response.status_code == 200

@pytest.mark.asyncio
async def test_synthesizer_concurrent_requests():
    text  =  "The time module has a function sleep() that you can use to suspend execution of the calling thread for however many seconds you specify."
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=fastAPI), base_url="http://testserver") as client:
        tasks = [ client.get("/synthesizer", params={"model_id": "speecht5", "speaker_id":7306, "language": "ENG", "text": text}) for i in range(30)]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "audio/wav"
        assert response.headers["Content-Disposition"] == "attachment; filename=output.wav"
        assert len(response.content) > 0

# @pytest.mark.asyncio
# async def test_synthesizer_concurrent_requests():
#     async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
#         tasks = [ client.get("/synthesizer", params={"model_id": "vits", "language": "ENG", "text": f"Hello, world! {i}"}) for i in range(25)]
#         responses = await asyncio.gather(*tasks)

#     for response in responses:
#         assert response.status_code == 200
#         assert response.headers["Content-Type"] == "audio/wav"
#         assert response.headers["Content-Disposition"] == "attachment; filename=output.wav"
#         assert len(response.content) > 0
