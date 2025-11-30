from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, status

from contracts import AuctionResponse, AuctionsListQuery, AuctionsListResponse
from core.dependency_injection import Container
from services import AuctionsService

router = APIRouter(prefix="/api/v1")


@router.get("/auctions", status_code=status.HTTP_200_OK, operation_id="get_auctions_list")
@inject
async def get_auctions_list(
    request: Annotated[AuctionsListQuery, Query()],
    service: Annotated[AuctionsService, Depends(Provide[Container.auctions_service])],
) -> AuctionsListResponse:
    return await service.get_newest_auctions(request)


@router.get("/auctions/{auction_id}", status_code=status.HTTP_200_OK, operation_id="get_auction")
@inject
async def get_auction(
    auction_id: int,
    service: Annotated[AuctionsService, Depends(Provide[Container.auctions_service])],
) -> AuctionResponse:
    return await service.get_auction(auction_id)
