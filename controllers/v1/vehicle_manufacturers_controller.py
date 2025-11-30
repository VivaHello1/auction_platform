from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from contracts import (
    VehicleManufacturerRequest,
    VehicleManufacturerResponse,
    VehicleManufacturersResponse,
    VehicleModelRequest,
    VehicleModelResponse,
    VehicleModelsResponse,
)
from core.dependency_injection import Container
from services import VehicleManufacturersService

router = APIRouter(prefix="/api/v1")


@router.get("/manufacturers", status_code=status.HTTP_200_OK, operation_id="get_manufacturers")
@inject
async def get_manufacturers(
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
    query: Annotated[str | None, Query(alias="q", description="Search manufacturers by name")] = None,
) -> VehicleManufacturersResponse:

    return await service.get_manufacturers(query)


@router.post("/manufacturers", status_code=status.HTTP_201_CREATED, operation_id="create_manufacturer")
@inject
async def create_manufacturer(
    manufacturer: VehicleManufacturerRequest,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
) -> VehicleManufacturerResponse:

    return await service.create_manufacturer(manufacturer)


@router.put("/manufacturers/{manufacturer_id}", status_code=status.HTTP_200_OK, operation_id="update_manufacturer")
@inject
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer: VehicleManufacturerRequest,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
) -> VehicleManufacturerResponse:

    return await service.update_manufacturer(manufacturer_id, manufacturer)


@router.get(
    "/manufacturers/{manufacturer_id}/models", status_code=status.HTTP_200_OK, operation_id="get_models_by_manufacturer"
)
@inject
async def get_models_by_manufacturer(
    manufacturer_id: int,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
    query: Annotated[str | None, Query(alias="q", description="Search models by name")] = None,
) -> VehicleModelsResponse:

    return await service.get_models_by_manufacturer(manufacturer_id, query)


@router.get("/models/{model_id}", status_code=status.HTTP_200_OK, operation_id="get_model_by_id")
@inject
async def get_models_by_id(
    model_id: int,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
) -> VehicleModelResponse:

    return await service.get_model_by_id(model_id)


@router.post(
    "/manufacturers/{manufacturer_id}/models", status_code=status.HTTP_201_CREATED, operation_id="create_model"
)
@inject
async def create_model(
    manufacturer_id: int,
    model: VehicleModelRequest,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
) -> VehicleModelResponse:

    return await service.create_model(manufacturer_id, model)


@router.put(
    "/manufacturers/{manufacturer_id}/models/{model_id}",
    status_code=status.HTTP_200_OK,
    operation_id="update_model",
)
@inject
async def update_model(
    manufacturer_id: int,
    model_id: int,
    model: VehicleModelRequest,
    service: Annotated[VehicleManufacturersService, Depends(Provide[Container.vehicle_manufacturer_service])],
) -> VehicleModelResponse:

    return await service.update_model(manufacturer_id, model_id, model)
