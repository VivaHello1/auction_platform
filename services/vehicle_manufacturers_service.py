import asyncio

from contracts import (
    VehicleManufacturerRequest,
    VehicleManufacturerResponse,
    VehicleManufacturersResponse,
    VehicleModelRequest,
    VehicleModelResponse,
    VehicleModelsResponse,
)
from exceptions.types import NotFoundError
from mappers import VehicleManufacturerMapper, VehicleModelMapper
from repositories import VehicleManufacturersRepository, VehicleModelsRepository
from repositories.models import VehicleManufacturer as VehicleManufacturerRepositoryModel
from repositories.models import VehicleModel as VehicleModelRepositoryModel


class VehicleManufacturersService:
    def __init__(
        self, manufacturers_repository: VehicleManufacturersRepository, models_repository: VehicleModelsRepository
    ):
        self.manufacturers_repository = manufacturers_repository
        self.models_repository = models_repository

    async def get_manufacturers(self, query: str | None = None) -> VehicleManufacturersResponse:
        manufacturers = await self.manufacturers_repository.get_by_name(query)
        return VehicleManufacturerMapper.to_manufacturers_response(manufacturers)

    async def create_manufacturer(self, manufacturer: VehicleManufacturerRequest) -> VehicleManufacturerResponse:
        if not manufacturer.name:
            raise ValueError("Manufacturer name is required")

        synonyms = list(set(manufacturer.synonyms))
        new_manufacturer = await self.manufacturers_repository.create(
            VehicleManufacturerRepositoryModel(
                name=manufacturer.name,
                synonyms=synonyms,
            )
        )

        return VehicleManufacturerMapper.to_manufacturer_response(new_manufacturer)

    async def update_manufacturer(
        self, manufacturer_id: int, manufacturer: VehicleManufacturerRequest
    ) -> VehicleManufacturerResponse:
        existing_manufacturer = await self.manufacturers_repository.get_by_id(manufacturer_id)

        if not existing_manufacturer:
            raise NotFoundError(manufacturer_id, "Vehicle Manufacturer")

        existing_manufacturer.name = manufacturer.name or existing_manufacturer.name

        if manufacturer.synonyms is not None:
            existing_manufacturer.synonyms = list(set(manufacturer.synonyms))

        updated_manufacturer = await self.manufacturers_repository.update(
            existing_manufacturer,
        )

        return VehicleManufacturerMapper.to_manufacturer_response(updated_manufacturer)

    async def get_models_by_manufacturer(self, manufacturer_id: int, query: str | None = None) -> VehicleModelsResponse:
        manufacturer, models = await asyncio.gather(
            self.manufacturers_repository.get_by_id(manufacturer_id),
            self.models_repository.get_by_manufacturer_id_query(manufacturer_id, query),
        )

        if not manufacturer:
            raise NotFoundError(manufacturer_id, "Vehicle Manufacturer")

        return VehicleModelMapper.to_models_response(manufacturer, models)

    async def get_model_by_id(self, model_id: int) -> VehicleModelResponse:
        model = await self.models_repository.get_by_id(model_id)

        if not model:
            raise NotFoundError(model_id, "Vehicle Model")

        manufacturer = await self.manufacturers_repository.get_by_id(model.manufacturer_id) if model else None

        if not manufacturer:
            raise NotFoundError(model.manufacturer_id, "Vehicle Manufacturer")

        return VehicleModelMapper.to_model_response(model, manufacturer)

    async def create_model(self, manufacturer_id: int, model: VehicleModelRequest) -> VehicleModelResponse:
        manufacturer = await self.manufacturers_repository.get_by_id(manufacturer_id)

        if not manufacturer:
            raise NotFoundError(manufacturer_id, "Vehicle Manufacturer")

        if not model.name or not model.default_vehicle_type:
            raise ValueError("Model name and default vehicle type are required")

        synonyms = list(set(model.synonyms))
        new_model = await self.models_repository.create(
            VehicleModelRepositoryModel(
                name=model.name,
                default_vehicle_type=model.default_vehicle_type,
                synonyms=synonyms,
                manufacturer_id=manufacturer_id,
            )
        )

        return VehicleModelMapper.to_model_response(new_model, manufacturer)

    async def update_model(
        self, manufacturer_id: int, model_id: int, model: VehicleModelRequest
    ) -> VehicleModelResponse:
        existing_model = await self.models_repository.get_by_id(model_id)

        if not existing_model or existing_model.manufacturer_id != manufacturer_id:
            raise NotFoundError(model_id, "Vehicle Model")

        existing_model.name = model.name or existing_model.name
        existing_model.default_vehicle_type = model.default_vehicle_type or existing_model.default_vehicle_type

        if model.synonyms is not None:
            existing_model.synonyms = list(set(model.synonyms))

        updated_model = await self.models_repository.update(existing_model)

        manufacturer = await self.manufacturers_repository.get_by_id(manufacturer_id)

        return VehicleModelMapper.to_model_response(updated_model, manufacturer)
