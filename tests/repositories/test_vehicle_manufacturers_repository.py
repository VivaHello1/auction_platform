import pytest

from repositories import VehicleManufacturersRepository
from repositories.models import VehicleManufacturer
from tests.factories.vehicle_manufacturer_factory import VehicleManufacturerFactory


@pytest.fixture(scope="function")
def repository(clean_db, container) -> VehicleManufacturersRepository:
    return container.vehicle_manufacturers_repository()


class TestVehicleManufacturersRepository:
    async def test_get_by_name_without_query(self, repository: VehicleManufacturersRepository):
        # Create manufacturers
        VehicleManufacturerFactory.create(name="BMW", synonyms=["Bayerische Motoren Werke"])
        VehicleManufacturerFactory.create(name="Mercedes-Benz", synonyms=["Mercedes", "Benz"])
        VehicleManufacturerFactory.create(name="Audi", synonyms=["Audi AG"])

        actual = await repository.get_by_name()

        assert len(actual) == 3
        # Verify ordering by name
        assert actual[0].name == "Audi"
        assert actual[1].name == "BMW"
        assert actual[2].name == "Mercedes-Benz"

    @pytest.mark.parametrize(
        "search_query,expected_count,expected_names",
        [
            ("BMW", 1, ["BMW"]),
            ("Mer", 1, ["Mercedes-Benz"]),
            ("A", 1, ["Audi"]),
            ("nonexistent", 0, []),
            ("bMw", 1, ["BMW"]),  # Case insensitive
        ],
    )
    async def test_get_by_name_with_query(
        self,
        repository: VehicleManufacturersRepository,
        search_query: str,
        expected_count: int,
        expected_names: list[str],
    ):
        # Create manufacturers
        VehicleManufacturerFactory.create(name="BMW", synonyms=["Bayerische Motoren Werke"])
        VehicleManufacturerFactory.create(name="Mercedes-Benz", synonyms=["Mercedes", "Benz"])
        VehicleManufacturerFactory.create(name="Audi", synonyms=["Audi AG"])

        actual = await repository.get_by_name(search_query)

        assert len(actual) == expected_count
        actual_names = [manufacturer.name for manufacturer in actual]
        assert actual_names == expected_names

    async def test_get_by_name_empty_result(self, repository: VehicleManufacturersRepository):
        actual = await repository.get_by_name()

        assert len(actual) == 0

    async def test_get_by_id_existing(self, repository: VehicleManufacturersRepository):
        manufacturer = VehicleManufacturerFactory.create(name="Toyota", synonyms=["Toyota Motor Corporation"])

        actual = await repository.get_by_id(manufacturer.id)

        assert actual is not None
        assert actual.id == manufacturer.id
        assert actual.name == "Toyota"
        assert actual.synonyms == ["Toyota Motor Corporation"]

    async def test_get_by_id_non_existing(self, repository: VehicleManufacturersRepository):
        actual = await repository.get_by_id(999)

        assert actual is None

    async def test_create_manufacturer(self, repository: VehicleManufacturersRepository):
        new_manufacturer = VehicleManufacturer(name="Ford", synonyms=["Ford Motor Company", "Ford Motors"])

        actual = await repository.create(new_manufacturer)

        assert actual.id is not None
        assert actual.name == "Ford"
        assert actual.synonyms == ["Ford Motor Company", "Ford Motors"]
        assert actual.created_at is not None

        # Verify it was actually saved to database
        saved_manufacturer = await repository.get_by_id(actual.id)
        assert saved_manufacturer is not None
        assert saved_manufacturer.name == "Ford"

    async def test_update_manufacturer(self, repository: VehicleManufacturersRepository):
        # Create a manufacturer first
        manufacturer = VehicleManufacturerFactory.create(name="Volkswagen", synonyms=["VW"])

        # Update the manufacturer
        manufacturer.name = "Volkswagen Group"
        manufacturer.synonyms = ["VW", "Volkswagen AG"]

        actual = await repository.update(manufacturer)

        assert actual.id == manufacturer.id
        assert actual.name == "Volkswagen Group"
        assert actual.synonyms == ["VW", "Volkswagen AG"]

        # Verify it was actually updated in database
        updated_manufacturer = await repository.get_by_id(manufacturer.id)
        assert updated_manufacturer.name == "Volkswagen Group"
        assert updated_manufacturer.synonyms == ["VW", "Volkswagen AG"]

    async def test_create_manufacturer_with_empty_synonyms(self, repository: VehicleManufacturersRepository):
        new_manufacturer = VehicleManufacturer(name="Tesla", synonyms=[])

        actual = await repository.create(new_manufacturer)

        assert actual.id is not None
        assert actual.name == "Tesla"
        assert actual.synonyms == []

    async def test_get_by_name_partial_match(self, repository: VehicleManufacturersRepository):
        await repository.create(VehicleManufacturer(name="General Motors", synonyms=["GM"]))
        await repository.create(VehicleManufacturer(name="Ford Motor Company", synonyms=["Ford"]))

        actual = await repository.get_by_name("Motor")

        assert len(actual) == 2
        manufacturer_names = [m.name for m in actual]
        assert "General Motors" in manufacturer_names
        assert "Ford Motor Company" in manufacturer_names
