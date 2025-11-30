from contracts import AuctionVehicle, AuctionVehicleFacet, ClientBid

from repositories.views import AuctionVehicleView, FacetView


class AuctionVehicleMapper:
    @staticmethod
    def to_contract(auction_vehicle_view: AuctionVehicleView) -> AuctionVehicle:
        return AuctionVehicle(
            vehicle_id=auction_vehicle_view.vehicle.id,
            is_active=auction_vehicle_view.vehicle.active,
            manufacturer=str(auction_vehicle_view.manufacturer.name),
            model=str(auction_vehicle_view.model.name),
            manufacturing_date=auction_vehicle_view.vehicle.manufacturing_date,
            mileage=auction_vehicle_view.vehicle.mileage,
            engine=auction_vehicle_view.vehicle.engine,
            transmission=auction_vehicle_view.vehicle.transmission,
            vin=auction_vehicle_view.vehicle.vin,
            images=auction_vehicle_view.vehicle.image_list,
        )

    @staticmethod
    def to_contract_list(auction_vehicle_views: list[AuctionVehicleView]) -> list[AuctionVehicle]:
        return [AuctionVehicleMapper.to_contract(view) for view in auction_vehicle_views]

    @staticmethod
    def to_contract_with_bids(auction_vehicle_view: AuctionVehicleView) -> AuctionVehicle:

        latest_bid = None

        return AuctionVehicle(
            vehicle_id=auction_vehicle_view.vehicle.id,
            is_active=auction_vehicle_view.vehicle.active,
            manufacturer=str(auction_vehicle_view.manufacturer.name),
            model=str(auction_vehicle_view.model.name),
            manufacturing_date=auction_vehicle_view.vehicle.manufacturing_date,
            mileage=auction_vehicle_view.vehicle.mileage,
            engine=auction_vehicle_view.vehicle.engine,
            transmission=auction_vehicle_view.vehicle.transmission,
            vin=auction_vehicle_view.vehicle.vin,
            client_bid=latest_bid,
            images=auction_vehicle_view.vehicle.image_list,
        )

    @staticmethod
    def to_contract_list_with_bids(auction_vehicle_views: list[AuctionVehicleView]) -> list[AuctionVehicle]:
        latest_bid_by_vehicle_id = {}

        # Sort auction vehicle views by last bid date (most recent first)
        # Vehicles with no bids will appear at the end
        sorted_views = sorted(
            auction_vehicle_views,
            key=lambda view: (
                latest_bid_by_vehicle_id[view.vehicle.id].created_at.timestamp()
                if view.vehicle.id in latest_bid_by_vehicle_id
                else 0
            ),
            reverse=True,
        )

        return [
            AuctionVehicleMapper.to_contract_with_bids(
                view, [latest_bid_by_vehicle_id[view.vehicle.id]] if view.vehicle.id in latest_bid_by_vehicle_id else []
            )
            for view in sorted_views
        ]

    @staticmethod
    def facet_to_contract(facet_view: FacetView) -> AuctionVehicleFacet:
        """Map FacetView to AuctionVehicleFacet contract"""
        return AuctionVehicleFacet(
            id=facet_view.id,
            name=facet_view.name,
            count=facet_view.count,
        )

    @staticmethod
    def facets_to_contract(facet_views: list[FacetView]) -> list[AuctionVehicleFacet]:
        """Map list of FacetView to list of AuctionVehicleFacet contracts"""
        return [AuctionVehicleMapper.facet_to_contract(facet) for facet in facet_views]
