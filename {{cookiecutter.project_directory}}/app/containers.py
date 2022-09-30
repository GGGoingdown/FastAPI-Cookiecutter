from dependency_injector import containers, providers

# Application
from app import services, db, repositories
from app.config import Settings


class Gateway(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis_client = providers.Resource(db.redis_init)

    db_resource = providers.Resource(db.DBResource, config=db.TORTOISE_ORM)


class Service(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()
    gateway = providers.DependenciesContainer()
    # * Resource Initialize * #
    logger_init = providers.Resource(
        services.LoggerInitialize,
        application_name=config.app.application_name,
        log_level=config.app.log_level,
        env_mode=config.app.env_mode,
        log_path=config.app.log_path,
    )

    # * Model Repositories *#
    user_repo = providers.Singleton(
        repositories.UserRepo,
    )

    # * Auth Services *#
    jwt_handler = providers.Singleton(
        services.JWTHandler,
        secret_key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm,
        expired_time_minute=config.jwt.expire_min,
    )

    authencation_seletor = providers.Singleton(
        services.AuthenticationSelector, jwt=jwt_handler
    )

    authentication_service = providers.Singleton(
        services.AuthenticationService,
        user_repo=user_repo,
        auth_selector=authencation_seletor,
    )

    authorization_service = providers.Singleton(
        services.AuthorizationService,
        auth_selector=authencation_seletor,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateway = providers.Container(Gateway, config=config)
    service = providers.Container(Service, config=config, gateway=gateway)
