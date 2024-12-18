import asyncio
import time

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/v1",
    tags=["sse"],
    responses={404: {"description": "Not found"}},
)

events = []


# Simulated data stream for SSE
@router.get("/sse")
async def sse_endpoint():
    async def event_generator():
        while True:
            # Simulate a real-time update
            await asyncio.sleep(5)
            if events:
                yield f"data: {events.pop(0)}\n\n"
            else:
                yield f"data: No new events\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/add-event")
async def add_event():
    events.append("New event")
    return {"message": "Event added"}
