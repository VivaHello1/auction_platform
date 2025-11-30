from sqlalchemy import select

from repositories.base_repository import BaseRepository
from repositories.models import VehicleModel


class VehicleModelsRepository(BaseRepository):
    async def get_by_name(self, query: str | None = None) -> list[VehicleModel]:
        query = (
            select(VehicleModel)
            .where(VehicleModel.name.ilike(f"%{query}%") if query else True)
            .order_by(VehicleModel.name)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_manufacturer_id_query(self, manufacturer_id: int, query: str | None = None) -> list[VehicleModel]:
        query = (
            select(VehicleModel)
            .where(
                VehicleModel.manufacturer_id == manufacturer_id,
                VehicleModel.name.ilike(f"%{query}%") if query else True,
            )
            .order_by(VehicleModel.name)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_id(self, model_id: int) -> VehicleModel | None:
        query = select(VehicleModel).where(VehicleModel.id == model_id)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create(self, model: VehicleModel) -> VehicleModel:
        async with self.session_factory() as session:
            session.add(model)
            await session.commit()

        return model

    async def update(self, model: VehicleModel) -> VehicleModel:
        async with self.session_factory() as session:
            merged_model = await session.merge(model)
            await session.commit()

            return merged_model
