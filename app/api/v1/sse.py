import asyncio
import time

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/v1",
    tags=["sse"],
    responses={404: {"description": "Not found"}},
)


# Simulated data stream for SSE
@router.get("/sse")
async def sse_endpoint():
    async def event_generator():
        while True:
            # Simulate a real-time update
            await asyncio.sleep(1)
            yield f"data: Update at {time.time()}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
