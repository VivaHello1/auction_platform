from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from contracts import AuctionVehicleResponse, AuctionVehiclesQuery, AuctionVehiclesResponse, AuctionVehicleUpdateRequest
from core.dependency_injection import Container
from services import AuctionVehiclesService

router = APIRouter(prefix="/api/v1")


@router.get("/auction-vehicles/{auction_id}", status_code=200, operation_id="get_auction_vehicles_list")
@inject
async def get_auction_vehicles_list(
    auction_id: int,
    request: Annotated[AuctionVehiclesQuery, Query()],
    service: Annotated[AuctionVehiclesService, Depends(Provide[Container.auction_vehicles_service])],
) -> AuctionVehiclesResponse:

    return await service.get_auction_vehicles_list(auction_id, request)


@router.put("/auction-vehicles/{vehicle_id}", status_code=200, operation_id="update_auction_vehicle")
@inject
async def update_auction_vehicle(
    vehicle_id: int,
    request: AuctionVehicleUpdateRequest,
    service: Annotated[AuctionVehiclesService, Depends(Provide[Container.auction_vehicles_service])],
) -> AuctionVehicleResponse:
    return await service.update_auction_vehicle(vehicle_id, request)
