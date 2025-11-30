from datetime import UTC, datetime

from contracts import Auction, AuctionCarPreview
from repositories.models import Auction as AuctionModel
from repositories.views import AuctionVehicleView


class AuctionMapper:
    @staticmethod
    def to_contract(auction: AuctionModel, car_preview: list[AuctionCarPreview], car_count: int = 0) -> Auction:
        return Auction(
            id=auction.id,
            name=auction.name,
            country=auction.country,
            car_count=car_count,
            close_date=auction.end_datetime,
            status='active' if auction.end_datetime > datetime.now(UTC) else 'closed',
            car_preview=car_preview,
        )

    @staticmethod
    def to_contract_list(
        auctions: list[AuctionModel], car_previews: dict[int, list[AuctionCarPreview]], car_counts: dict[int, int]
    ) -> list[Auction]:
        auction_contracts = [
            AuctionMapper.to_contract(auction, car_previews.get(auction.id, []), car_counts.get(auction.id, 0))
            for auction in auctions
        ]
        auction_contracts.sort(key=lambda auction: (auction.status == 'closed', auction.close_date))

        return auction_contracts

    @staticmethod
    def to_car_preview_list(vehicles: list[AuctionVehicleView]) -> list[AuctionCarPreview]:
        return [
            AuctionCarPreview(
                id=vehicle.vehicle.id,
                manufacturer_id=vehicle.manufacturer.id,
                manufacturer=vehicle.manufacturer.name,
                model_id=vehicle.model.id,
                model=vehicle.model.name,
                manufacturing_date=vehicle.vehicle.manufacturing_date,
                mileage=vehicle.vehicle.mileage,
            )
            for vehicle in vehicles
        ]
