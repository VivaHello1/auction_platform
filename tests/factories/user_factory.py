from datetime import UTC, datetime
from random import random
from uuid import uuid4

import factory

from repositories.models.user import User
from tests import test_container


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_container.db().sync_session()
        sqlalchemy_session_persistence = 'commit'

    id = factory.LazyFunction(uuid4)
    supervisor_id = factory.LazyFunction(lambda: uuid4() if random() < 0.2 else None)
    phone_number = factory.Sequence(lambda n: f"+1{(n + 2000000000) % 10000000000:010d}")
    passport_number = factory.Faker("uuid4")
    address = factory.Faker("address")
    language = factory.Faker("random_element", elements=["en", "de", "es", "fr"])
    email = factory.Faker("email")
    registration_date = factory.LazyFunction(lambda: datetime.now(UTC))
    comments = factory.List([factory.Faker("text", max_nb_chars=100) for _ in range(2)])
    status = factory.Faker("random_element", elements=["active", "inactive", "pending"])
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
    updated_at = factory.LazyFunction(lambda: datetime.now(UTC))
