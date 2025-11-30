import uuid

from sqlalchemy import select

from repositories.base_repository import BaseRepository

from .models import User


class UsersRepository(BaseRepository):
    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        async with self.session_factory() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        async with self.session_factory() as session:
            merged_user = await session.merge(user)
            await session.commit()

            return merged_user

    async def create(self, user: User) -> User:
        async with self.session_factory() as session:
            session.add(user)
            await session.commit()

            return user
