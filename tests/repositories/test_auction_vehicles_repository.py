import pytest

from repositories.auction_vehicles_repository import AuctionVehiclesRepository
from tests.factories.auction_factory import AuctionFactory
from tests.factories.auction_vehicle_factory import AuctionVehicleFactory
from tests.factories.vehicle_manufacturer_factory import VehicleManufacturerFactory
from tests.factories.vehicle_model_factory import VehicleModelFactory


@pytest.fixture(scope="function")
def repository(clean_db, container) -> AuctionVehiclesRepository:
    return container.auction_vehicles_repository()


class TestAuctionVehiclesRepository:
    @pytest.mark.parametrize(
        "_from,size",
        [
            (0, 10),
            (1, 5),
        ],
    )
    async def test_get_by_auction_id(self, repository: AuctionVehiclesRepository, _from: int, size: int):
        # Create auction and vehicles
        auction = AuctionFactory.create()
        manufacturer = VehicleManufacturerFactory.create()
        model = VehicleModelFactory.create(manufacturer_id=manufacturer.id)

        # Create vehicles for this auction
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)

        # Create vehicle for different auction (should not be returned)
        other_auction = AuctionFactory.create()
        AuctionVehicleFactory.create(auction_id=other_auction.id, manufacturer_id=manufacturer.id, model_id=model.id)

        actual = await repository.get_by_auction_id(auction.id, _from, size)

        assert len(actual) <= size
        if _from == 0:
            assert len(actual) == min(3, size)

        # Verify all returned vehicles belong to the correct auction
        for vehicle_view in actual:
            assert vehicle_view.vehicle.auction_id == auction.id
            assert vehicle_view.manufacturer.id == manufacturer.id
            assert vehicle_view.model.id == model.id

    async def test_get_by_auction_id_with_filters(self, repository: AuctionVehiclesRepository):
        # Create auction and related entities
        auction = AuctionFactory.create()
        manufacturer = VehicleManufacturerFactory.create()
        model = VehicleModelFactory.create(manufacturer_id=manufacturer.id)

        # Create vehicles with different types
        AuctionVehicleFactory.create(
            auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id, type="car"
        )
        AuctionVehicleFactory.create(
            auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id, type="truck"
        )

        # Test type filter
        filters = {"type": "car"}
        actual = await repository.get_by_auction_id(auction.id, _from=0, size=10, **filters)

        assert len(actual) == 1
        assert actual[0].vehicle.type == "car"

    async def test_get_by_auction_id_count(self, repository: AuctionVehiclesRepository):
        # Create auction and related entities
        auction = AuctionFactory.create()
        manufacturer = VehicleManufacturerFactory.create()
        model = VehicleModelFactory.create(manufacturer_id=manufacturer.id)

        # Create vehicles for this auction
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id)

        # Create vehicle for different auction (should not be counted)
        other_auction = AuctionFactory.create()
        AuctionVehicleFactory.create(auction_id=other_auction.id, manufacturer_id=manufacturer.id, model_id=model.id)

        actual = await repository.get_by_auction_id_count(auction.id)

        assert actual == 3

    async def test_get_car_counts_by_auction_ids(self, repository: AuctionVehiclesRepository):
        # Create auctions and related entities
        auction1 = AuctionFactory.create()
        auction2 = AuctionFactory.create()
        auction3 = AuctionFactory.create()
        manufacturer = VehicleManufacturerFactory.create()
        model = VehicleModelFactory.create(manufacturer_id=manufacturer.id)

        # Create vehicles for different auctions
        # Auction 1: 2 vehicles
        AuctionVehicleFactory.create(auction_id=auction1.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction1.id, manufacturer_id=manufacturer.id, model_id=model.id)

        # Auction 2: 3 vehicles
        AuctionVehicleFactory.create(auction_id=auction2.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction2.id, manufacturer_id=manufacturer.id, model_id=model.id)
        AuctionVehicleFactory.create(auction_id=auction2.id, manufacturer_id=manufacturer.id, model_id=model.id)

        # Auction 3: 0 vehicles (no vehicles created)

        actual = await repository.get_car_counts_by_auction_ids([auction1.id, auction2.id, auction3.id])

        assert actual[auction1.id] == 2
        assert actual[auction2.id] == 3
        assert auction3.id not in actual  # No vehicles, so not in result

    async def test_get_by_auction_id_empty_result(self, repository: AuctionVehiclesRepository):
        auction = AuctionFactory.create()

        actual = await repository.get_by_auction_id(auction.id, _from=0, size=10)

        assert len(actual) == 0

    async def test_get_car_counts_empty_auction_ids(self, repository: AuctionVehiclesRepository):
        actual = await repository.get_car_counts_by_auction_ids([])

        assert actual == {}

    async def test_get_car_counts_nonexistent_auction_ids(self, repository: AuctionVehiclesRepository):
        actual = await repository.get_car_counts_by_auction_ids([999, 1000])

        assert actual == {}

    async def test_get_by_auction_id_with_range_filters(self, repository: AuctionVehiclesRepository):
        # Create auction and related entities
        auction = AuctionFactory.create()
        manufacturer = VehicleManufacturerFactory.create()
        model = VehicleModelFactory.create(manufacturer_id=manufacturer.id)

        # Create vehicles with different mileage values
        _ = AuctionVehicleFactory.create(
            auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id, mileage=50000
        )
        _ = AuctionVehicleFactory.create(
            auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id, mileage=100000
        )
        _ = AuctionVehicleFactory.create(
            auction_id=auction.id, manufacturer_id=manufacturer.id, model_id=model.id, mileage=150000
        )

        # Test mileage greater than or equal filter
        filters = {"mileage__gte": 100000}
        actual = await repository.get_by_auction_id(auction.id, _from=0, size=10, **filters)
        assert len(actual) == 2
        mileages = [v.vehicle.mileage for v in actual]
        assert all(m >= 100000 for m in mileages)

        # Test mileage less than or equal filter
        filters = {"mileage__lte": 100000}
        actual = await repository.get_by_auction_id(auction.id, _from=0, size=10, **filters)
        assert len(actual) == 2
        mileages = [v.vehicle.mileage for v in actual]
        assert all(m <= 100000 for m in mileages)

        # Test mileage between filter
        filters = {"mileage__between": [75000, 125000]}
        actual = await repository.get_by_auction_id(auction.id, _from=0, size=10, **filters)
        assert len(actual) == 1
        assert actual[0].vehicle.mileage == 100000

        # Test count method with range filters
        filters = {"mileage__gte": 100000}
        count = await repository.get_by_auction_id_count(auction.id, **filters)
        assert count == 2
