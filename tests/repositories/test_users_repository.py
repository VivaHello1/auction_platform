import uuid

import pytest

from repositories.users_repository import UsersRepository
from tests.factories.user_factory import UserFactory


@pytest.fixture(scope="function")
def repository(clean_db, container) -> UsersRepository:
    return container.users_repository()


class TestUsersRepository:
    async def test_get_existing_user(self, repository: UsersRepository):
        user = UserFactory.create(email="test@example.com", status="active")

        actual = await repository.get_by_id(user.id)

        assert actual is not None
        assert actual.id == user.id
        assert actual.email == "test@example.com"
        assert actual.status == "active"

    async def test_get_nonexistent_user(self, repository: UsersRepository):
        actual = await repository.get_by_id(uuid.uuid4())

        assert actual is None

    async def test_update_user(self, repository: UsersRepository):
        user = UserFactory.create(email="original@example.com", status="active")

        user.email = "updated@example.com"
        user.status = "inactive"

        updated_user = await repository.update(user)

        assert updated_user.id == user.id
        assert updated_user.email == "updated@example.com"
        assert updated_user.status == "inactive"

        # Verify the update persisted
        retrieved_user = await repository.get_by_id(user.id)
        assert retrieved_user.email == "updated@example.com"
        assert retrieved_user.status == "inactive"
        assert retrieved_user.status == "inactive"
