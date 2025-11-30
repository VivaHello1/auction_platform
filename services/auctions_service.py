import asyncio
from datetime import date

from contracts import AuctionCarPreview, AuctionResponse, AuctionsListQuery, AuctionsListResponse
from exceptions.types import NotFoundError
from mappers import AuctionMapper
from repositories import AuctionsRepository, AuctionVehiclesRepository


class AuctionsService:
    def __init__(self, auctions_repository: AuctionsRepository, auction_vehicles_repository: AuctionVehiclesRepository):
        self.auctions_repository = auctions_repository
        self.auction_vehicles_repository = auction_vehicles_repository

    async def get_newest_auctions(self, request: AuctionsListQuery) -> AuctionsListResponse:
        filters = {
            "country": request.country if request.country else None,
            "status": request.status if request.status else None,
            "datetime": date.today(),
        }

        auctions, auctions_total = await asyncio.gather(
            self.auctions_repository.get_newest(_from=request.from_, size=request.size, **filters),
            self.auctions_repository.get_newest_count(**filters),
        )

        auction_ids = [auction.id for auction in auctions]
        car_counts = await self.auction_vehicles_repository.get_car_counts_by_auction_ids(auction_ids)
        car_previews = await self._get_car_previews(auction_ids)

        auctions_list = AuctionMapper.to_contract_list(auctions, car_previews, car_counts)
        auctions_list.sort(key=lambda auction: (auction.status == 'closed', auction.close_date))

        return AuctionsListResponse(
            total=auctions_total,
            items=auctions_list,
        )

    async def get_auction(self, auction_id: int) -> AuctionResponse:
        auction = await self.auctions_repository.get_by_id(auction_id)

        if not auction:
            raise NotFoundError(auction_id, "Auction")

        car_counts = await self.auction_vehicles_repository.get_car_counts_by_auction_ids([auction.id])

        return AuctionResponse(
            auction=AuctionMapper.to_contract(auction, [], car_counts.get(auction.id, 0)),
        )

    async def _get_car_previews(self, auction_ids: list[int]) -> dict[int, list[AuctionCarPreview]]:
        tasks = [self._get_preview_cars(auction_id) for auction_id in auction_ids]
        results = await asyncio.gather(*tasks)

        return dict(zip(auction_ids, results, strict=False))

    async def _get_preview_cars(self, auction_id) -> list[AuctionCarPreview]:
        cars = await self.auction_vehicles_repository.get_by_auction_id(auction_id, _from=0, size=5, active=True)
        return AuctionMapper.to_car_preview_list(cars)
