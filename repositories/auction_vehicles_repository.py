from sqlalchemy import extract, func, select

from repositories.models import AuctionVehicle, VehicleManufacturer, VehicleModel
from repositories.views import (
    AuctionVehicleSchema,
    AuctionVehicleView,
    FacetView,
    VehicleManufacturerSchema,
    VehicleModelSchema,
)

from .base_repository import BaseRepository


class AuctionVehiclesRepository(BaseRepository):
    async def get_by_auction_id(self, auction_id: int, _from: int, size: int, **kwargs) -> list[AuctionVehicleView]:
        query = (
            select(AuctionVehicle, VehicleManufacturer, VehicleModel)
            .where(AuctionVehicle.auction_id == auction_id)
            .join(VehicleManufacturer, AuctionVehicle.manufacturer_id == VehicleManufacturer.id)
            .join(VehicleModel, AuctionVehicle.model_id == VehicleModel.id)
            .offset(_from)
            .limit(size)
        )

        query = self._apply_filters(query, kwargs, AuctionVehicle)

        async with self.session_factory() as session:
            result = await session.execute(query)
            rows = result.all()

            return [
                AuctionVehicleView(
                    vehicle=AuctionVehicleSchema.model_validate(vehicle),
                    manufacturer=VehicleManufacturerSchema.model_validate(manufacturer),
                    model=VehicleModelSchema.model_validate(model),
                )
                for vehicle, manufacturer, model in rows
            ]

    async def get_by_auction_id_count(self, auction_id: int, **kwargs) -> int:
        query = select(func.count()).select_from(AuctionVehicle).where(AuctionVehicle.auction_id == auction_id)
        query = self._apply_filters(query, kwargs, AuctionVehicle)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalar()

    async def get_by_id(self, vehicle_id: int) -> AuctionVehicle | None:
        query = (
            select(AuctionVehicle, VehicleManufacturer, VehicleModel)
            .where(AuctionVehicle.id == vehicle_id)
            .join(VehicleManufacturer, AuctionVehicle.manufacturer_id == VehicleManufacturer.id)
            .join(VehicleModel, AuctionVehicle.model_id == VehicleModel.id)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_view_by_id(self, vehicle_id: int) -> AuctionVehicleView | None:
        query = (
            select(AuctionVehicle, VehicleManufacturer, VehicleModel)
            .where(AuctionVehicle.id == vehicle_id)
            .join(VehicleManufacturer, AuctionVehicle.manufacturer_id == VehicleManufacturer.id)
            .join(VehicleModel, AuctionVehicle.model_id == VehicleModel.id)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            row = result.first()

            if not row:
                return None

            vehicle, manufacturer, model = row
            return AuctionVehicleView(
                vehicle=AuctionVehicleSchema.model_validate(vehicle),
                manufacturer=VehicleManufacturerSchema.model_validate(manufacturer),
                model=VehicleModelSchema.model_validate(model),
            )

    async def get_car_counts_by_auction_ids(self, auction_ids: list[int]) -> dict[int, int]:
        query = (
            select(AuctionVehicle.auction_id, func.count())
            .where(AuctionVehicle.auction_id.in_(auction_ids))
            .group_by(AuctionVehicle.auction_id)
        )

        async with self.session_factory() as session:
            result = await session.execute(query)
            return {row[0]: row[1] for row in result.all()}

    async def create(self, vehicle: AuctionVehicle) -> AuctionVehicle:
        async with self.session_factory() as session:
            session.add(vehicle)
            await session.commit()

            return vehicle

    async def get_manufacturer_facets(self, auction_id: int, **kwargs) -> list[FacetView]:
        """Get manufacturer facets with ID, name and count for vehicles in an auction"""
        filters = {**kwargs, 'auction_id': auction_id}

        query = (
            select(VehicleManufacturer.id, VehicleManufacturer.name, func.count().label("count"))
            .join(AuctionVehicle, AuctionVehicle.manufacturer_id == VehicleManufacturer.id)
            .group_by(VehicleManufacturer.id, VehicleManufacturer.name)
            .order_by(VehicleManufacturer.name)
        )
        query = self._apply_filters(query, filters, AuctionVehicle)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return [
                FacetView(id=manufacturer_id, name=name, count=count) for manufacturer_id, name, count in result.all()
            ]

    async def get_model_facets(self, auction_id: int, **kwargs) -> list[FacetView]:
        """Get model facets with ID, name and count for vehicles in an auction"""
        filters = {**kwargs, 'auction_id': auction_id}

        query = (
            select(VehicleModel.id, VehicleModel.name, func.count().label("count"))
            .join(AuctionVehicle, AuctionVehicle.model_id == VehicleModel.id)
            .group_by(VehicleModel.id, VehicleModel.name)
            .order_by(VehicleModel.name)
        )
        query = self._apply_filters(query, filters, AuctionVehicle)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return [FacetView(id=model_id, name=name, count=count) for model_id, name, count in result.all()]

    async def get_registration_year_facets(self, auction_id: int, **kwargs) -> list[FacetView]:
        """Get registration year facets for vehicles in an auction"""
        filters = {**kwargs, 'auction_id': auction_id}

        query = (
            select(extract('year', AuctionVehicle.manufacturing_date), func.count().label("count"))
            .group_by(extract('year', AuctionVehicle.manufacturing_date))
            .order_by(extract('year', AuctionVehicle.manufacturing_date))
        )
        query = self._apply_filters(query, filters, AuctionVehicle)

        async with self.session_factory() as session:
            result = await session.execute(query)
            return [FacetView(id=None, name=str(int(year)), count=count) for year, count in result.all()]

    async def update(self, vehicle: AuctionVehicle) -> AuctionVehicle:
        async with self.session_factory() as session:
            db_vehicle = await session.merge(vehicle)

            await session.flush()
            await session.refresh(db_vehicle)
            await session.commit()

            return db_vehicle

            await session.flush()
            await session.refresh(db_vehicle)
            await session.commit()

            return db_vehicle

            await session.flush()
            await session.refresh(db_vehicle)
            await session.commit()

            return db_vehicle
