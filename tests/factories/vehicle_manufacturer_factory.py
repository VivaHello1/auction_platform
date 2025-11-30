import factory

from repositories.models.vehicle_manufacturer import VehicleManufacturer
from tests import test_container


class VehicleManufacturerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = VehicleManufacturer
        sqlalchemy_session = test_container.db().sync_session()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Sequence(lambda n: f"Manufacturer_{n}")
    synonyms = factory.LazyFunction(lambda: [])
