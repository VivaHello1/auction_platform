from dependency_injector import containers, providers


from database.database import Database
from repositories import (
    AuctionsRepository,
    AuctionVehiclesRepository,
    UsersRepository,
    VehicleManufacturersRepository,
    VehicleModelsRepository,
)
from services import (
    AuctionsService,
    AuctionVehiclesService,
    UsersService,
    VehicleManufacturersService,
)

from .config import settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])

    wiring_config = containers.WiringConfiguration(packages=["controllers.v1", "controllers"])

    db = providers.Singleton(
        Database,
        db_url=config.postgres.DATABASE_URL,
        schema=config.postgres.POSTGRES_SCHEMA,
    )

    # Repositories
    auctions_repository = providers.Factory(
        AuctionsRepository,
        session_factory=db.provided.session_factory,
    )
    auction_vehicles_repository = providers.Factory(
        AuctionVehiclesRepository,
        session_factory=db.provided.session_factory,
    )
    vehicle_manufacturers_repository = providers.Factory(
        VehicleManufacturersRepository,
        session_factory=db.provided.session_factory,
    )
    vehicle_models_repository = providers.Factory(
        VehicleModelsRepository,
        session_factory=db.provided.session_factory,
    )
    users_repository = providers.Factory(
        UsersRepository,
        session_factory=db.provided.session_factory,
    )

    # Services
    auctions_service = providers.Factory(
        AuctionsService,
        auctions_repository=auctions_repository,
        auction_vehicles_repository=auction_vehicles_repository,
    )
    auction_vehicles_service = providers.Factory(
        AuctionVehiclesService,
        auction_vehicles_repository=auction_vehicles_repository,
        vehicle_manufacturers_repository=vehicle_manufacturers_repository,
        vehicle_models_repository=vehicle_models_repository,
    )
    vehicle_manufacturer_service = providers.Factory(
        VehicleManufacturersService,
        manufacturers_repository=vehicle_manufacturers_repository,
        models_repository=vehicle_models_repository,
    )
    users_service = providers.Factory(
        UsersService,
        users_repository=users_repository,
    )


def create_container(app_settings=settings):
    container = Container()
    container.config.from_pydantic(app_settings)
    return container
