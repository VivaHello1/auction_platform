import pytest

from repositories.models import VehicleManufacturer, VehicleModel
from repositories.vehicle_models_repository import VehicleModelsRepository


@pytest.fixture(scope="function")
def repository(clean_db, container) -> VehicleModelsRepository:
    return container.vehicle_models_repository()


class TestVehicleModelsRepository:

    async def test_get_by_name_without_query(self, repository: VehicleModelsRepository):
        # Create manufacturers first
        bmw = await repository.create(VehicleManufacturer(id=1, name="BMW", synonyms=["BMW"]))
        mercedes = await repository.create(VehicleManufacturer(id=2, name="Mercedes-Benz", synonyms=["Mercedes"]))

        # Create vehicle models
        await repository.create(
            VehicleModel(
                name="3 Series", manufacturer_id=bmw.id, default_vehicle_type="sedan", synonyms=["320i", "330i"]
            )
        )
        await repository.create(
            VehicleModel(name="X3", manufacturer_id=bmw.id, default_vehicle_type="suv", synonyms=["BMW X3"])
        )
        await repository.create(
            VehicleModel(
                name="C-Class", manufacturer_id=mercedes.id, default_vehicle_type="sedan", synonyms=["C200", "C220"]
            )
        )

        actual = await repository.get_by_name()

        assert len(actual) == 3
        # Verify ordering by name
        assert actual[0].name == "3 Series"
        assert actual[1].name == "C-Class"
        assert actual[2].name == "X3"

    @pytest.mark.parametrize(
        "search_query,expected_count,expected_names",
        [
            ("3 Series", 1, ["3 Series"]),
            ("C-", 1, ["C-Class"]),
            ("X", 1, ["X3"]),
            ("Series", 1, ["3 Series"]),
            ("nonexistent", 0, []),
            ("series", 1, ["3 Series"]),  # Case insensitive
        ],
    )
    async def test_get_by_name_with_query(
        self, repository: VehicleModelsRepository, search_query: str, expected_count: int, expected_names: list[str]
    ):
        # Create manufacturer first
        bmw = await repository.create(VehicleManufacturer(id=1, name="BMW", synonyms=["BMW"]))
        mercedes = await repository.create(VehicleManufacturer(id=2, name="Mercedes-Benz", synonyms=["Mercedes"]))

        # Create vehicle models
        await repository.create(
            VehicleModel(
                name="3 Series", manufacturer_id=bmw.id, default_vehicle_type="sedan", synonyms=["320i", "330i"]
            )
        )
        await repository.create(
            VehicleModel(name="X3", manufacturer_id=bmw.id, default_vehicle_type="suv", synonyms=["BMW X3"])
        )
        await repository.create(
            VehicleModel(
                name="C-Class", manufacturer_id=mercedes.id, default_vehicle_type="sedan", synonyms=["C200", "C220"]
            )
        )

        actual = await repository.get_by_name(search_query)

        assert len(actual) == expected_count
        actual_names = [model.name for model in actual]
        assert actual_names == expected_names

    async def test_get_by_name_empty_result(self, repository: VehicleModelsRepository):
        actual = await repository.get_by_name()

        assert len(actual) == 0

    async def test_get_by_manufacturer_id_query_without_query(self, repository: VehicleModelsRepository):
        # Create manufacturers first
        bmw = await repository.create(VehicleManufacturer(id=1, name="BMW", synonyms=["BMW"]))
        mercedes = await repository.create(VehicleManufacturer(id=2, name="Mercedes-Benz", synonyms=["Mercedes"]))

        # Create vehicle models
        await repository.create(
            VehicleModel(
                name="3 Series", manufacturer_id=bmw.id, default_vehicle_type="sedan", synonyms=["320i", "330i"]
            )
        )
        await repository.create(
            VehicleModel(name="X3", manufacturer_id=bmw.id, default_vehicle_type="suv", synonyms=["BMW X3"])
        )
        await repository.create(
            VehicleModel(
                name="C-Class", manufacturer_id=mercedes.id, default_vehicle_type="sedan", synonyms=["C200", "C220"]
            )
        )

        actual = await repository.get_by_manufacturer_id_query(bmw.id)

        assert len(actual) == 2
        # Verify ordering by name and all are BMW models
        assert actual[0].name == "3 Series"
        assert actual[1].name == "X3"
        assert all(model.manufacturer_id == bmw.id for model in actual)

    @pytest.mark.parametrize(
        "search_query,expected_count,expected_names",
        [
            ("X", 1, ["X3"]),
            ("Series", 1, ["3 Series"]),
            ("nonexistent", 0, []),
            ("series", 1, ["3 Series"]),  # Case insensitive
        ],
    )
    async def test_get_by_manufacturer_id_query_with_query(
        self, repository: VehicleModelsRepository, search_query: str, expected_count: int, expected_names: list[str]
    ):
        # Create manufacturer first
        bmw = await repository.create(VehicleManufacturer(id=1, name="BMW", synonyms=["BMW"]))
        mercedes = await repository.create(VehicleManufacturer(id=2, name="Mercedes-Benz", synonyms=["Mercedes"]))

        # Create vehicle models
        await repository.create(
            VehicleModel(
                name="3 Series", manufacturer_id=bmw.id, default_vehicle_type="sedan", synonyms=["320i", "330i"]
            )
        )
        await repository.create(
            VehicleModel(name="X3", manufacturer_id=bmw.id, default_vehicle_type="suv", synonyms=["BMW X3"])
        )
        await repository.create(
            VehicleModel(
                name="C-Class", manufacturer_id=mercedes.id, default_vehicle_type="sedan", synonyms=["C200", "C220"]
            )
        )

        actual = await repository.get_by_manufacturer_id_query(bmw.id, search_query)

        assert len(actual) == expected_count
        actual_names = [model.name for model in actual]
        assert actual_names == expected_names

    async def test_get_by_manufacturer_id_query_non_existing_manufacturer(self, repository: VehicleModelsRepository):
        actual = await repository.get_by_manufacturer_id_query(999)

        assert len(actual) == 0

    async def test_get_by_id_existing(self, repository: VehicleModelsRepository):
        # Create manufacturer first
        bmw = await repository.create(VehicleManufacturer(id=1, name="BMW", synonyms=["BMW"]))

        # Create vehicle model
        model = await repository.create(
            VehicleModel(
                name="5 Series", manufacturer_id=bmw.id, default_vehicle_type="sedan", synonyms=["520i", "530i"]
            )
        )

        actual = await repository.get_by_id(model.id)

        assert actual is not None
        assert actual.id == model.id
        assert actual.name == "5 Series"
        assert actual.manufacturer_id == bmw.id
        assert actual.default_vehicle_type == "sedan"
        assert actual.synonyms == ["520i", "530i"]

    async def test_get_by_id_non_existing(self, repository: VehicleModelsRepository):
        actual = await repository.get_by_id(999)

        assert actual is None

    async def test_create_vehicle_model(self, repository: VehicleModelsRepository):
        # Create manufacturer first
        toyota = await repository.create(VehicleManufacturer(id=1, name="Toyota", synonyms=["Toyota"]))

        new_model = VehicleModel(
            name="Corolla",
            manufacturer_id=toyota.id,
            default_vehicle_type="sedan",
            synonyms=["Toyota Corolla", "Corolla Sedan"],
        )

        actual = await repository.create(new_model)

        assert actual.id is not None
        assert actual.name == "Corolla"
        assert actual.manufacturer_id == toyota.id
        assert actual.default_vehicle_type == "sedan"
        assert actual.synonyms == ["Toyota Corolla", "Corolla Sedan"]
        assert actual.created_at is not None

        # Verify it was actually saved to database
        saved_model = await repository.get_by_id(actual.id)
        assert saved_model is not None
        assert saved_model.name == "Corolla"

    async def test_update_vehicle_model(self, repository: VehicleModelsRepository):
        # Create manufacturer first
        audi = await repository.create(VehicleManufacturer(id=1, name="Audi", synonyms=["Audi"]))

        # Create a vehicle model first
        model = await repository.create(
            VehicleModel(name="A4", manufacturer_id=audi.id, default_vehicle_type="sedan", synonyms=["Audi A4"])
        )

        # Update the model
        model.name = "A4 Allroad"
        model.default_vehicle_type = "wagon"
        model.synonyms = ["Audi A4 Allroad", "A4 Quattro"]

        actual = await repository.update(model)

        assert actual.id == model.id
        assert actual.name == "A4 Allroad"
        assert actual.default_vehicle_type == "wagon"
        assert actual.synonyms == ["Audi A4 Allroad", "A4 Quattro"]

        # Verify it was actually updated in database
        updated_model = await repository.get_by_id(model.id)
        assert updated_model.name == "A4 Allroad"
        assert updated_model.default_vehicle_type == "wagon"
        assert updated_model.synonyms == ["Audi A4 Allroad", "A4 Quattro"]

    async def test_create_vehicle_model_with_empty_synonyms(self, repository: VehicleModelsRepository):
        # Create manufacturer first
        ford = await repository.create(VehicleManufacturer(id=1, name="Ford", synonyms=["Ford"]))

        new_model = VehicleModel(name="Focus", manufacturer_id=ford.id, default_vehicle_type="hatchback", synonyms=[])

        actual = await repository.create(new_model)

        assert actual.id is not None
        assert actual.name == "Focus"
        assert actual.manufacturer_id == ford.id
        assert actual.default_vehicle_type == "hatchback"
        assert actual.synonyms == []

    async def test_get_by_name_partial_match(self, repository: VehicleModelsRepository):
        # Create manufacturer first
        volkswagen = await repository.create(VehicleManufacturer(id=1, name="Volkswagen", synonyms=["VW"]))

        await repository.create(
            VehicleModel(
                name="Golf GTI",
                manufacturer_id=volkswagen.id,
                default_vehicle_type="hatchback",
                synonyms=["VW Golf GTI"],
            )
        )
        await repository.create(
            VehicleModel(
                name="Golf R", manufacturer_id=volkswagen.id, default_vehicle_type="hatchback", synonyms=["VW Golf R"]
            )
        )

        actual = await repository.get_by_name("Golf")

        assert len(actual) == 2
        model_names = [m.name for m in actual]
        assert "Golf GTI" in model_names
        assert "Golf R" in model_names
