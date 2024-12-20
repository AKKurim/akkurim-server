import asyncio
import json
import time

from fastapi import APIRouter, Request, Response
from sse_starlette.sse import EventSourceResponse

from app.schemas.sse_event import SSEEvent
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


# convert the message to an json string
@router.post("/add-event")
async def add_event():
    """Sample endpoint to add an event to the SSE stream
    used for testing purposes

    Returns:
        _type_: _description_
    """
    message = SSEEvent(
        action="insert",
        table_name="guardian",
        object_id=1,
        object_data={"first_name": "John", "last_name": "Doe"},
    )
    await broadcast.publish(
        channel="updates",
        message=json.dumps(message.model_dump()),
    )
    return Response(status_code=200)
