import random
from datetime import date, timedelta

import factory

from repositories.models.auction_vehicle import AuctionVehicle
from tests import test_container
from tests.factories.auction_factory import AuctionFactory
from tests.factories.vehicle_manufacturer_factory import VehicleManufacturerFactory
from tests.factories.vehicle_model_factory import VehicleModelFactory


class AuctionVehicleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = AuctionVehicle
        sqlalchemy_session = test_container.db().sync_session()
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 9000000)
    external_id = factory.LazyAttribute(lambda obj: f"EXT-{obj.id}")
    auction_id = factory.LazyAttribute(lambda obj: AuctionFactory.create().id)
    manufacturer_id = factory.LazyAttribute(lambda obj: VehicleManufacturerFactory.create().id)
    model_id = factory.LazyAttribute(lambda obj: VehicleModelFactory.create().id)
    manufacturing_date = factory.LazyFunction(
        lambda: date.today() - timedelta(days=random.randint(365, 3650))
    )  # 1-10 years old
    type = factory.Faker("random_element", elements=["car", "truck", "motorcycle", "van", None])
    category = factory.Faker("random_element", elements=["economy", "compact", "mid-size", "luxury", "sports", None])
    mileage = factory.Faker("random_int", min=1000, max=200000)
    engine = factory.Faker("random_element", elements=["petrol", "diesel", "electric", "hybrid"])
    transmission = factory.Faker("random_element", elements=["manual", "automatic", "semi-automatic"])
    vin = factory.LazyFunction(lambda: ''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ0123456789', k=17)))
    body_type = factory.Faker(
        "random_element", elements=["sedan", "hatchback", "suv", "coupe", "convertible", "wagon", None]
    )
    color = factory.Faker("random_element", elements=["white", "black", "silver", "red", "blue", "gray", "green", None])
    engine_power = factory.Faker("random_int", min=50, max=500)  # HP
    engine_cc = factory.Faker("random_int", min=1000, max=5000)  # CC
    maintenance_url = factory.Faker("url")
    inspection_url = factory.Faker("url")
    start_price = factory.Faker("random_int", min=1000, max=50000)
    only_buy_now = factory.Faker("boolean", chance_of_getting_true=20)
    buy_now_price = factory.LazyAttribute(
        lambda obj: obj.start_price + random.randint(1000, 10000) if obj.only_buy_now else None
    )
    active = factory.Faker("boolean", chance_of_getting_true=90)
    is_commercial = factory.Faker("boolean", chance_of_getting_true=10)
    is_damaged = factory.Faker("boolean", chance_of_getting_true=15)
    number_plates = factory.Faker("license_plate")
    vehicle_url = factory.Faker("url")
    equipment = factory.LazyFunction(
        lambda: random.sample(
            [
                "air_conditioning",
                "cruise_control",
                "leather_seats",
                "sunroof",
                "navigation",
                "bluetooth",
                "parking_sensors",
                "heated_seats",
            ],
            random.randint(0, 4),
        )
    )
    description = factory.Faker("text", max_nb_chars=500)
    image_list = factory.LazyFunction(
        lambda: [f"https://example.com/image_{i}.jpg" for i in range(random.randint(1, 8))]
    )
    reference_url = factory.LazyAttribute(lambda obj: f"https://example.com/reference/{obj.id}")
