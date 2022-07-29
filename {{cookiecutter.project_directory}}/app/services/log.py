import sys
from loguru import logger
from dependency_injector import resources
from typing import Optional
from pathlib import Path

# Settings
from app.schemas import GenericSchema


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
            ...
            # TODO: Save file path

        return None

    def shutdown(self, log_file: Optional[Path] = None) -> None:
        if log_file and log_file.is_file():
            logger.info(f"Remove log: {log_file}")
            log_file.unlink(missing_ok=True)
