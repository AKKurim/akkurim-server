import asyncio
import time

from fastapi import APIRouter, Request, Response
from sse_starlette.sse import EventSourceResponse

from app.utils.broadcast import broadcast

router = APIRouter(
    prefix="/v1",
    tags=["sse"],
    responses={404: {"description": "Not found"}},
)

events = []


async def event_generator():
    async with broadcast.subscribe(channel="updates") as subscriber:
        while True:
            event = await subscriber.get()
            if event is None:
                break
            yield event


# Simulated data stream for SSE
@router.get("/sse")
async def sse_endpoint():
    return EventSourceResponse(event_generator())


@router.post("/add-event")
async def add_event():
    await broadcast.publish(
        channel="updates", message="New event at " + str(time.time())
    )
    return Response(status_code=200)
