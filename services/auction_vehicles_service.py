import asyncio

from contracts import (
    AuctionVehicleFacets,
    AuctionVehicleResponse,
    AuctionVehiclesQuery,
    AuctionVehiclesResponse,
    AuctionVehicleUpdateRequest,
)
from core.logging import logger
from exceptions.types import NotFoundError
from mappers import AuctionVehicleMapper
from repositories import (
    AuctionVehiclesRepository,
    VehicleManufacturersRepository,
    VehicleModelsRepository,
)
from repositories.models import User
from repositories.views import FacetView
from services.filters import AuctionVehicleFilterBuilder


class AuctionVehiclesService:
    def __init__(
        self,
        auction_vehicles_repository: AuctionVehiclesRepository,
        vehicle_manufacturers_repository: VehicleManufacturersRepository,
        vehicle_models_repository: VehicleModelsRepository,
    ):
        self.auction_vehicles_repository = auction_vehicles_repository
        self.vehicle_manufacturers_repository = vehicle_manufacturers_repository
        self.vehicle_models_repository = vehicle_models_repository

    async def get_auction_vehicles_list(
        self, auction_id: int, parameters: AuctionVehiclesQuery
    ) -> AuctionVehiclesResponse:
        filter_builder = AuctionVehicleFilterBuilder(parameters)
        filters = filter_builder.build_main_filters()

        auction_vehicles, auctions_total, vehicle_bids, facets = await asyncio.gather(
            self.auction_vehicles_repository.get_by_auction_id(
                auction_id=auction_id,
                _from=parameters.from_,
                size=parameters.size,
                **filters,
            ),
            self.auction_vehicles_repository.get_by_auction_id_count(
                auction_id=auction_id,
                **filters,
            ),
            self._get_facets(auction_id, parameters),
        )

        logger.info("user bids: %s", vehicle_bids)

        auction_vehicles_list = AuctionVehicleMapper.to_contract_list_with_bids(
            auction_vehicle_views=auction_vehicles,
        )

        return AuctionVehiclesResponse(
            total=auctions_total,
            items=auction_vehicles_list,
            facets=facets,
        )

    async def update_auction_vehicle(
        self, vehicle_id: int, request: AuctionVehicleUpdateRequest
    ) -> AuctionVehicleResponse:
        current_vehicle = await self.auction_vehicles_repository.get_by_id(vehicle_id)
        if not current_vehicle:
            raise NotFoundError(vehicle_id, "AuctionVehicle")

        if request.is_active is not None:
            current_vehicle.active = request.is_active
        if request.mileage is not None:
            current_vehicle.mileage = request.mileage
        if request.manufacturing_date is not None:
            current_vehicle.manufacturing_date = request.manufacturing_date
        if request.engine is not None:
            current_vehicle.engine = request.engine
        if request.transmission is not None:
            current_vehicle.transmission = request.transmission
        if request.vin is not None:
            current_vehicle.vin = request.vin

        if request.manufacturer_id is not None:
            manufacturer = await self.vehicle_manufacturers_repository.get_by_id(request.manufacturer_id)
            if not manufacturer:
                raise NotFoundError(request.manufacturer_id, "VehicleManufacturer")
            current_vehicle.manufacturer_id = manufacturer.id

        if request.model_id is not None:
            model = await self.vehicle_models_repository.get_by_id(request.model_id)
            if not model:
                raise NotFoundError(request.model_id, "VehicleModel")
            current_vehicle.model_id = model.id

        vehicle = await self.auction_vehicles_repository.update(current_vehicle)
        vehicle_view = await self.auction_vehicles_repository.get_view_by_id(vehicle.id)

        return AuctionVehicleResponse(vehicle=AuctionVehicleMapper.to_contract(vehicle_view))

    async def _get_facets(self, auction_id: int, parameters: AuctionVehiclesQuery) -> AuctionVehicleFacets:
        filter_builder = AuctionVehicleFilterBuilder(parameters)

        # Get selected manufacturer and model data to preserve them in facets
        selected_manufacturers = await self._get_selected_manufacturers(parameters.manufacturer_ids)
        selected_models = await self._get_selected_models(parameters.model_ids)
        selected_years = (
            list(range(parameters.registration_year_from or 0, (parameters.registration_year_to or 0) + 1))
            if parameters.registration_year_from and parameters.registration_year_to
            else []
        )

        # Get all facets concurrently with appropriate filters
        manufacturer_facets, model_facets, year_facets = await asyncio.gather(
            self.auction_vehicles_repository.get_manufacturer_facets(
                auction_id, **filter_builder.build_manufacturer_facet_filters()
            ),
            self.auction_vehicles_repository.get_model_facets(auction_id, **filter_builder.build_model_facet_filters()),
            self.auction_vehicles_repository.get_registration_year_facets(
                auction_id, **filter_builder.build_year_facet_filters()
            ),
        )

        merged_manufacturers = self._merge_selected_with_facets(selected_manufacturers, manufacturer_facets)
        merged_models = self._merge_selected_with_facets(selected_models, model_facets)

        selected_year_facets = [FacetView(id=None, name=str(year), count=0) for year in selected_years]
        merged_years = self._merge_selected_with_facets(selected_year_facets, year_facets)

        return AuctionVehicleFacets(
            manufacturers=AuctionVehicleMapper.facets_to_contract(merged_manufacturers),
            models=AuctionVehicleMapper.facets_to_contract(merged_models),
            registration_years=AuctionVehicleMapper.facets_to_contract(merged_years),
        )

    async def _get_selected_manufacturers(self, manufacturer_ids: list[int]) -> list[FacetView]:
        """Get manufacturer data for selected manufacturer IDs"""
        if not manufacturer_ids:
            return []

        manufacturers = await asyncio.gather(
            *[self.vehicle_manufacturers_repository.get_by_id(manufacturer_id) for manufacturer_id in manufacturer_ids]
        )
        return [
            FacetView(id=manufacturer.id, name=manufacturer.name, count=0)
            for manufacturer in manufacturers
            if manufacturer
        ]

    async def _get_selected_models(self, model_ids: list[int]) -> list[FacetView]:
        """Get model data for selected model IDs"""
        if not model_ids:
            return []

        models = await asyncio.gather(*[self.vehicle_models_repository.get_by_id(model_id) for model_id in model_ids])
        return [FacetView(id=model.id, name=model.name, count=0) for model in models if model]

    def _merge_selected_with_facets(
        self, selected_facets: list[FacetView], actual_facets: list[FacetView]
    ) -> list[FacetView]:
        """Merge selected facets (with count 0) with actual facet data"""
        # Create result dict starting with selected facets
        result = {}

        # Add selected facets first (with count 0)
        for facet in selected_facets:
            key = facet.id if facet.id is not None else facet.name
            result[key] = facet

        # Update with actual counts, overriding selected items
        for facet in actual_facets:
            key = facet.id if facet.id is not None else facet.name
            result[key] = facet

        return list(result.values())
