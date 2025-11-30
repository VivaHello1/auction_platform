from sqlalchemy import func, select

from repositories.base_repository import BaseRepository

from .models import Auction


class AuctionsRepository(BaseRepository):
    async def get_newest(self, _from: int, size: int, **kwargs) -> list[Auction]:
        query = select(Auction).offset(_from).limit(size).order_by(Auction.end_datetime.asc())
        query = self._apply_filters(query, kwargs, Auction)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def get_newest_count(self, **kwargs) -> int:
        query = select(func.count()).select_from(Auction)
        query = self._apply_filters(query, kwargs, Auction)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalar()

    async def get_by_id(self, auction_id: int) -> Auction | None:
        async with self.session_factory() as session:
            result = await session.execute(select(Auction).where(Auction.id == auction_id))
            return result.scalar_one_or_none()

    async def create(self, auction: Auction) -> Auction:
        async with self.session_factory() as session:
            session.add(auction)
            await session.commit()

        return auction
