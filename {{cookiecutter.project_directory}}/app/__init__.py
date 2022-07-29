#######
#   Application Metadata
#######
__VERSION__ = "v0.0.1"
__TITLE__ = "FastAPI Application"
__DESCRIPTION__ = "FastAPI Base Application"
__DOCS_URL__ = None
__ROOT_PATH__ = "/api/v1"
################################################
import sys
import sentry_sdk
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

# Settings
from app import exceptions
from app.config import settings

# Sentry
def add_sentry_middleware(app: FastAPI, *, release_name: str) -> None:
    from app.middleware import CustomSentryAsgiMiddleware

    # Initial sentry and add middleware
    logger.info("--- Initial Sentry ---")
    sentry_sdk.init(
        settings.sentry.dns,
        traces_sample_rate=settings.sentry.trace_sample_rates,
        release=f"{release_name}@{__VERSION__}",
        environment=settings.app.env_mode.value,
    )
    app.add_middleware(CustomSentryAsgiMiddleware)


# Exceptions
def add_exceptions(app: FastAPI) -> None:
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
        root_path=__ROOT_PATH__,
    )

    # Routers
    from app import routers

    app.include_router(routers.health_router)

    # Dependency injection
    from app.containers import Application

    container = Application()
    container.config.from_pydantic(settings)

    container.wire(modules=[sys.modules[__name__]])

    app.container = container

    @app.on_event("startup")
    async def startup_event():
        logger.info("--- Startup Event ---")
        await app.container.service.init_resources()

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("--- Shutdown Event ---")
        await app.container.service.shutdown_resources()

    # Sentry middleware
    if settings.sentry.dns:
        add_sentry_middleware(app, release_name=settings.app.application_name)

    # Customize Exceptions
    add_exceptions(app)

    return app
