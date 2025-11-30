import random
from datetime import UTC, datetime, timedelta

import factory

from repositories.models.auction import Auction
from tests import test_container


class AuctionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Auction
        sqlalchemy_session = test_container.db().sync_session()
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 90000)
    name = factory.Faker("company")
    type = factory.Faker("random_element", elements=["online", "live", "sealed_bid"])
    leasing_company_id = factory.Faker("random_int", min=1, max=1000)
    reference_url = factory.Faker("url")
    country = factory.Faker("country_code")
    end_datetime = factory.LazyFunction(lambda: datetime.now(UTC) + timedelta(days=random.randint(1, 30)))
