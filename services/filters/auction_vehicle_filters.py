from datetime import date

from contracts import AuctionVehiclesQuery


class AuctionVehicleFilterBuilder:
    """Builds filter dictionaries for auction vehicle queries"""

    def __init__(self, parameters: AuctionVehiclesQuery):
        self.parameters = parameters

    def build_base_filters(self) -> dict:
        """Build base filters excluding facet-specific ones (manufacturer_id, model_id)"""
        filters = {}

        if self.parameters.is_active is not None:
            filters["active"] = self.parameters.is_active

        # Mileage range filters
        if self.parameters.mileage_from is not None:
            filters["mileage__gte"] = self.parameters.mileage_from
        if self.parameters.mileage_to is not None:
            filters["mileage__lte"] = self.parameters.mileage_to

        # Manufacturing date (registration year) range filters
        if self.parameters.registration_year_from is not None:
            filters["manufacturing_date__gte"] = date(self.parameters.registration_year_from, 1, 1)
        if self.parameters.registration_year_to is not None:
            filters["manufacturing_date__lte"] = date(self.parameters.registration_year_to, 12, 31)

        return filters

    def build_main_filters(self) -> dict:
        """Build filters for main query (includes all filters)"""
        filters = self.build_base_filters()

        if self.parameters.model_ids:
            filters["model_id"] = self.parameters.model_ids
        if self.parameters.manufacturer_ids:
            filters["manufacturer_id"] = self.parameters.manufacturer_ids

        return filters

    def build_manufacturer_facet_filters(self) -> dict:
        """Build filters for manufacturer facets (exclude manufacturer filter)"""
        filters = self.build_base_filters()

        if self.parameters.model_ids:
            filters["model_id"] = self.parameters.model_ids

        return filters

    def build_model_facet_filters(self) -> dict:
        """Build filters for model facets (exclude model filter)"""
        filters = self.build_base_filters()

        if self.parameters.manufacturer_ids:
            filters["manufacturer_id"] = self.parameters.manufacturer_ids

        return filters

    def build_year_facet_filters(self) -> dict:
        """Build filters for year facets (include all filters)"""
        return self.build_main_filters()
