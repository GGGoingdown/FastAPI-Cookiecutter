import sys
import logging
import ecs_logging
from loguru import logger
from dependency_injector import resources
from typing import Optional
from pathlib import Path

# Settings
from app import utils
from app.schemas import GenericSchema, LogSchema


class LoggerInitialize(resources.Resource):
    def init(
        self,
        application_name: str,
        log_level: GenericSchema.LogLevel = GenericSchema.LogLevel.DEUBG,
        env_mode: GenericSchema.EnvironmentMode = GenericSchema.EnvironmentMode.DEV,
        log_path: Optional[str] = None,
    ) -> Optional[Path]:
        #! WARNING: Logger remove must at the begin of logger initialize !#
        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<green>{time:YYYY-MM-DDTHH:mm:ss}</green> |<y>[{level}]</y> | <e>{file}::{function}::{line}</e> | {message}",
            level=log_level.value,
        )
        logger.info(
            f"--- [{application_name}]::Logger initialize in {env_mode.value} mode success ---"
        )

        if log_path:
            _path = Path(log_path) / application_name
            if not _path.is_dir():
                logger.info(f"Create log folder: {_path}")
                _path.mkdir(parents=True, exist_ok=False)

            uniquie_id = utils.get_shortuuid()
            now = utils.get_utc_now()
            dt_format = now.strftime("%Y-%m-%d")
            log_file = _path / f"system-{dt_format}-{uniquie_id}.json"
            logger.info(f"Create log file: {log_file}")
            ecs_handler = logging.FileHandler(str(log_file))
            ecs_handler.setFormatter(
                ecs_logging.StdlibFormatter(
                    exclude_fields=[
                        "process",
                        "level.icon",
                        "log.origin",
                        "log.original",
                        "log.logger",
                    ]
                )
            )

            if env_mode != GenericSchema.EnvironmentMode.TEST:
                logger.add(
                    ecs_handler,
                    format="[{extra[env_mode]}][{extra[provider]}] - [{extra[method]}] - {extra[path]} - [{extra[response_status_code]}] - {extra[response_body]}",
                    filter="app.middleware",
                    level="INFO",
                    enqueue=True,
                )
                logger.configure(
                    extra=LogSchema.EcsInitializeLogSchema(
                        provider=application_name, env_mode=env_mode
                    ).dict()
                )

            return log_file

        return None

    def shutdown(self, log_file: Optional[Path] = None) -> None:
        if log_file and log_file.is_file():
            logger.info(f"Remove log: {log_file}")
            log_file.unlink(missing_ok=True)
