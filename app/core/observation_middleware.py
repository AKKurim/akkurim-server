import time

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging import logger


class ObservationMiddleware:

    app: ASGIApp

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        status_code = None

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                nonlocal status_code
                status_code = message["status"]
                headers = MutableHeaders(scope=message)
                headers.append("X-Process-Time", str(time.perf_counter() - start_time))

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            # TODO maybe do something with the exception
            logger.exception(e)
            raise
        finally:
            if scope["path"] == "/":
                return
            process_time = time.perf_counter() - start_time
            logger.info(
                f"Request {scope['method']} {scope['path']}, code {status_code}, processed in {process_time:.6f}s"
            )
