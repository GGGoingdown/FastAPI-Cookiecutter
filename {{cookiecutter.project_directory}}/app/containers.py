from dependency_injector import containers, providers

# Application
from app import services, db
from app.config import Settings


class Gateway(containers.DeclarativeContainer):
    config = providers.Configuration()
    # Redis
    redis_client = providers.Resource(db.redis_init)
    # DB
    db_resource = providers.Resource(db.DBResource, config=db.TORTOISE_ORM)


class Service(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()
    gateway = providers.DependenciesContainer()

    logger_init = providers.Resource(
        services.LoggerInitialize, application_name=config.app.application_name
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateway = providers.Container(Gateway, config=config)
    service = providers.Container(Service, config=config, gateway=gateway)
