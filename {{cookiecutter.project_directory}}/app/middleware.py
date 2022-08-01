import json
from loguru import logger
from typing import TYPE_CHECKING, Any, Optional, Tuple, List, Dict
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi.routing import APIRoute
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.routing import Match
from dataclasses import dataclass
from sentry_sdk import capture_exception

if TYPE_CHECKING:
    from sentry_sdk._types import Event, Hint

# Schemas
from app.schemas.log import EcsBaseLogSchema


class CustomSentryAsgiMiddleware(SentryAsgiMiddleware):
    def event_processor(
        self, event: "Event", hint: "Hint", asgi_scope: Any
    ) -> "Optional[Event]":
        result_event = super().event_processor(event, hint, asgi_scope)
        route: Optional[APIRoute] = asgi_scope.get("route")
        if route and result_event:
            result_event["transaction"] = route.path
        return result_event


@dataclass
class IgnoredRoute:
    path: str
    method: Optional[str] = None


@dataclass
class OverwriteRouteBody:
    path: str
    body: Dict
    method: Optional[str] = None


class LogRequestsMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        ignored_routes: List[IgnoredRoute] = [],
        overwrite_routes_body: List[OverwriteRouteBody] = [],
    ) -> None:
        self.app = app
        self.ignore_routes = ignored_routes
        self.overwrite_routes_body = overwrite_routes_body

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            responder = _RequestLoggingResponder(
                self.app,
                ignored_routes=self.ignore_routes,
                overwrite_routes_body=self.overwrite_routes_body,
            )
            await responder(scope, receive, send)
            return

        await self.app(scope, receive, send)


class _RequestLoggingResponder:
    def __init__(
        self,
        app: ASGIApp,
        ignored_routes: List[IgnoredRoute],
        overwrite_routes_body: List[OverwriteRouteBody],
    ) -> None:
        self.app = app
        self.receive: Receive = unattached_receive
        self.send: Send = unattached_send
        self._ignored_routes = ignored_routes
        self._overwrite_routes_body = overwrite_routes_body
        self._path: str = ""
        self._method: str = ""
        self._request_body: bytearray = bytearray()
        self._response_body: bytearray = bytearray()
        self._response_status_code = None
        self._x_real_ip_header = None
        self._x_error_header = None
        self._x_room = None
        self._x_task = None
        self._authorization_header = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.receive = receive
        self.send = send

        request = Request(scope)

        path_tempalte, is_handled_path = self.get_path_template(request)
        if self._should_ignore_request(
            request_method=request.method,
            path_tempalte=path_tempalte,
            is_handled_path=is_handled_path,
        ):
            await self.app(scope, self.receive, self.send)
            return

        self.should_overwrite_response_body = self._should_overwrite_response(
            request_method=request.method,
            path_tempalte=path_tempalte,
            is_handled_path=is_handled_path,
        )

        self._method = request.method
        self._path = request.url.path
        headers = Headers(scope=scope)

        self._x_real_ip_header = headers.get("X-Real-ip", None)
        self._authorization_header = headers.get("Authorization", None)

        self.should_log_request_body = "application/json" in headers.get(
            "content-type", ""
        )

        await self.app(scope, self.receive_with_logging, self.send_with_logging)

        self._safe_log_request_response()

    async def receive_with_logging(self) -> Message:
        message = await self.receive()

        if message["type"] != "http.request":
            return message

        if not self.should_log_request_body:
            return message

        body: bytes = message.get("body", b"")
        self._request_body.extend(body)

        return message

    async def send_with_logging(self, message: Message) -> None:

        if message["type"] == "http.response.start":
            self._response_status_code = message.get("status")
            headers = Headers(raw=message["headers"])
            # Detail error message
            self._x_error_header = headers.get("X-Error", None)

            self.should_log_response_body = "application/json" in headers.get(
                "content-type", ""
            )
            await self.send(message)

        elif message["type"] == "http.response.body":
            if not self.should_log_response_body:
                await self.send(message)
                return

            if self.should_overwrite_response_body:
                await self.send(message)
                return

            body: bytes = message.get("body", b"")
            self._response_body.extend(body)
            await self.send(message)

    def _safe_log_request_response(self):
        try:
            request_body = self._request_body and json.loads(self._request_body)
            response_body = self._response_body and json.loads(self._response_body)

            _log_schema = EcsBaseLogSchema(
                path=self._path,
                method=self._method,
                request_body=request_body,
                response_body=response_body,
                response_status_code=self._response_status_code,
                x_real_ip=self._x_real_ip_header,
                x_error=self._x_error_header,
            )
            context_logger = logger.bind(**_log_schema.dict())
            stdout_format = f"{[self._response_status_code]} - {self._x_error_header or ''} - {response_body}"
            if self._response_status_code in [500, 501, 502]:
                context_logger.error(stdout_format)
            else:
                context_logger.info(stdout_format)

        except Exception as e:
            logger.error(e)
            capture_exception(e)
            pass

    def _should_ignore_request(
        self, *, request_method: str, path_tempalte: str, is_handled_path: bool
    ) -> bool:
        if not is_handled_path:
            return False

        for ignored_route in self._ignored_routes:
            if path_tempalte == ignored_route.path and (
                ignored_route.method is None
                or ignored_route.method.lower() == request_method.lower()  # noqa: W503
            ):
                return True
        return False

    def _should_overwrite_response(
        self, *, request_method: str, path_tempalte: str, is_handled_path: bool
    ) -> bool:
        if not is_handled_path:
            return False

        for overwrite_route in self._overwrite_routes_body:
            if path_tempalte == overwrite_route.path and (
                overwrite_route.method is None
                or overwrite_route.method.lower()  # noqa: W503
                == request_method.lower()  # noqa: W503
            ):
                body = json.dumps(overwrite_route.body).encode("utf-8")
                self._response_body.extend(body)
                return True
        return False

    @staticmethod
    def get_path_template(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False


async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
