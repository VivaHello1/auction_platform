import factory

from repositories.models.vehicle_model import VehicleModel
from tests import test_container


class VehicleModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = VehicleModel
        sqlalchemy_session = test_container.db().sync_session()
        sqlalchemy_session_persistence = 'commit'

    manufacturer_id = factory.LazyAttribute(lambda obj: 1)  # Default value, can be overridden
    name = factory.Sequence(lambda n: f"Model_{n}")
    synonyms = factory.LazyFunction(lambda: [])  # Empty array by default
    default_vehicle_type = factory.Sequence(lambda n: f"Vehicle_type_{n}")
