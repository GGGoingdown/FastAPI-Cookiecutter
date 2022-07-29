from typing import TYPE_CHECKING, Any, Optional
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from fastapi.routing import APIRoute

if TYPE_CHECKING:
    from sentry_sdk._types import Event, Hint


class CustomSentryAsgiMiddleware(SentryAsgiMiddleware):
    def event_processor(
        self, event: "Event", hint: "Hint", asgi_scope: Any
    ) -> "Optional[Event]":
        result_event = super().event_processor(event, hint, asgi_scope)
        route: Optional[APIRoute] = asgi_scope.get("route")
        if route and result_event:
            result_event["transaction"] = route.path
        return result_event
