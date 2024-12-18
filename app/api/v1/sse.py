import asyncio
import time

from fastapi import APIRouter, Request, Response
from sse_starlette.sse import EventSourceResponse

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
                yield f"{events.pop(0)}\n\n"
            else:
                yield f"No new events\n\n"

    return EventSourceResponse(event_generator())


@router.post("/add-event")
async def add_event():
    events.append("New event")
    return {"message": "Event added"}
