from sqlalchemy import select

from repositories.base_repository import BaseRepository
from repositories.models import VehicleManufacturer


class VehicleManufacturersRepository(BaseRepository):
    async def get_by_name(self, query: str | None = None) -> list[VehicleManufacturer]:
        query = (
            select(VehicleManufacturer)
            .where(VehicleManufacturer.name.ilike(f"%{query}%") if query else True)
            .order_by(VehicleManufacturer.name)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_id(self, manufacturer_id: int) -> VehicleManufacturer | None:
        query = select(VehicleManufacturer).where(VehicleManufacturer.id == manufacturer_id)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, manufacturer: VehicleManufacturer) -> VehicleManufacturer:
        async with self.session_factory() as session:
            session.add(manufacturer)
            await session.commit()

        return manufacturer

    async def update(self, manufacturer: VehicleManufacturer) -> VehicleManufacturer:
        async with self.session_factory() as session:
            db_manufacturer = await session.merge(manufacturer)

            await session.flush()
            await session.refresh(db_manufacturer)
            await session.commit()

            return db_manufacturer
