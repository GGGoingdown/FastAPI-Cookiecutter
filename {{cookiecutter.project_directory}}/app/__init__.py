#######
#   Application Metadata
#######
__VERSION__ = "{{ cookiecutter.project_version }}"
__TITLE__ = "{{ cookiecutter.project_title }}"
__DESCRIPTION__ = "{{ cookiecutter.project_description }}"
__DOCS_URL__ = None
__ROOT_PATH__ = "{{ cookiecutter.project_root_path }}"
################################################
import sys
import sentry_sdk
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Settings
from app import exceptions
from app.config import settings

# Sentry
def add_sentry_middleware(app: FastAPI, *, release_name: str) -> None:
    from app.middleware import CustomSentryAsgiMiddleware

    def before_send(event, hint):
        if "exc_info" in hint:
            exc_type, exc_value, tb = hint["exc_info"]
            if isinstance(exc_value, ValueError):
                logger.warning(f"Exception: {exc_type} - Value: {exc_value}")
                return None
        return event

    # Initial sentry and add middleware
    logger.info("--- Initial Sentry ---")
    sentry_sdk.init(
        settings.sentry.dns,
        traces_sample_rate=settings.sentry.trace_sample_rates,
        release=f"{release_name}@{__VERSION__}",
        environment=settings.app.env_mode.value,
        before_send=before_send,
    )
    app.add_middleware(CustomSentryAsgiMiddleware)


# Log request
def add_log_middleware(app: FastAPI) -> None:
    from app.middleware import LogRequestsMiddleware, IgnoredRoute

    app.add_middleware(
        LogRequestsMiddleware,
        ignored_routes=[
            IgnoredRoute(path="/health"),  # Health check endpoint
            IgnoredRoute(path="/openapi.json"),  # OpenAPI
        ],
    )


# Exceptions
def add_exceptions(app: FastAPI) -> None:
    from tortoise.exceptions import DoesNotExist, IntegrityError

    @app.exception_handler(DoesNotExist)
    async def doesnotexist_exception_handler(request: Request, exc: DoesNotExist):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(IntegrityError)
    async def integrityerror_exception_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": [{"loc": [], "msg": str(exc), "type": "IntegrityError"}]
            },
        )

    @app.exception_handler(exceptions.BaseInternalServiceException)
    async def internalerror_exception_handler(
        request: Request, exc: exceptions.BaseInternalServiceException
    ):
        _error_message = str(exc.error_message)
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
            headers={"X-Error": _error_message},
        )


def create_app() -> FastAPI:
    app = FastAPI(
        title=__TITLE__,
        description=__DESCRIPTION__,
        version=__VERSION__,
        docs_url=__DOCS_URL__,
        # root_path=__ROOT_PATH__,
    )

    # Routers
    from app import routers

    app.include_router(routers.health_router)
    app.include_router(routers.authentication_router)
    app.include_router(routers.user_router)

    # Dependency injection
    from app import security
    from app.containers import Application

    container = Application()
    container.config.from_pydantic(settings)
    container.wire(modules=[sys.modules[__name__], security, routers.auth])

    app.container = container

    @app.on_event("startup")
    async def startup_event():
        logger.info("--- Startup Event ---")
        #! If resource with async function, change init_resources to await
        await app.container.service.init_resources()

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("--- Shutdown Event ---")
        #! If resource with async function, change init_resources to await
        await app.container.service.shutdown_resources()

    # Sentry middleware
    if settings.sentry.dns:
        add_sentry_middleware(app, release_name=settings.app.application_name)

    # Log request middleware
    add_log_middleware(app)

    # Customize Exceptions
    add_exceptions(app)

    return app
