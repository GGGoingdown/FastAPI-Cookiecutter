from dependency_injector import containers, providers

# Application
from app import services
from app.config import Settings


class Gateway(containers.DeclarativeContainer):
    config = providers.Configuration()


class Service(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()
    gateway = providers.DependenciesContainer()

    logger_init = providers.Resource(
        services.LoggerInitialize,
        application_name=config.app.application_name,
        log_level=config.app.log_level,
        env_mode=config.app.env_mode,
        log_path=config.app.log_path,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateway = providers.Container(Gateway, config=config)
    service = providers.Container(Service, config=config, gateway=gateway)
