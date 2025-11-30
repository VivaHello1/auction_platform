from contracts import (
    VehicleManufacturer,
    VehicleManufacturerResponse,
    VehicleManufacturersResponse,
    VehicleModel,
    VehicleModelResponse,
    VehicleModelsResponse,
)
from repositories.models import VehicleManufacturer as VehicleManufacturerRepositoryModel
from repositories.models import VehicleModel as VehicleModelRepositoryModel


class VehicleManufacturerMapper:
    @staticmethod
    def to_contract(manufacturer: VehicleManufacturerRepositoryModel) -> VehicleManufacturer:
        return VehicleManufacturer(
            id=manufacturer.id,
            name=manufacturer.name,
            synonyms=manufacturer.synonyms,
            created_at=manufacturer.created_at,
        )

    @staticmethod
    def to_manufacturers_response(
        manufacturers: list[VehicleManufacturerRepositoryModel],
    ) -> VehicleManufacturersResponse:
        return VehicleManufacturersResponse(
            manufacturers=[VehicleManufacturerMapper.to_contract(manufacturer) for manufacturer in manufacturers]
        )

    @staticmethod
    def to_manufacturer_response(manufacturer: VehicleManufacturerRepositoryModel) -> VehicleManufacturerResponse:
        return VehicleManufacturerResponse(manufacturer=VehicleManufacturerMapper.to_contract(manufacturer))


class VehicleModelMapper:
    @staticmethod
    def to_contract(model: VehicleModelRepositoryModel) -> VehicleModel:
        return VehicleModel(
            id=model.id,
            name=model.name,
            default_vehicle_type=model.default_vehicle_type,
            synonyms=model.synonyms,
            created_at=model.created_at,
        )

    @staticmethod
    def to_models_response(
        manufacturer: VehicleManufacturerRepositoryModel, models: list[VehicleModelRepositoryModel]
    ) -> VehicleModelsResponse:
        return VehicleModelsResponse(
            manufacturer=VehicleManufacturerMapper.to_contract(manufacturer),
            models=[VehicleModelMapper.to_contract(model) for model in models],
        )

    @staticmethod
    def to_model_response(
        model: VehicleModelRepositoryModel, manufacturer: VehicleManufacturerRepositoryModel
    ) -> VehicleModelResponse:
        return VehicleModelResponse(
            model=VehicleModelMapper.to_contract(model),
            manufacturer=VehicleManufacturerMapper.to_contract(manufacturer),
        )
