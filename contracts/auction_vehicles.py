from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from contracts.base import PaginatedResponse, PaginationParams


class ClientBid(BaseModel):
    client_id: int = Field(
        description="Unique identifier for the client",
        ge=1,
    )
    bid_amount: int = Field(
        description="Bid amount in the auction",
        gt=0,
    )
    bid_time: datetime = Field(
        description="Time when the bid was placed",
    )


class AuctionVehicle(BaseModel):
    vehicle_id: int = Field(
        description="Unique identifier for the auction vehicle 7 digits long",
        ge=1000000,
        le=9999999,
    )
    is_active: bool = Field(
        description="Indicates if the vehicle is currently active in the auction",
        default=True,
    )
    manufacturer: str = Field(
        description="Vehicle manufacturer name",
        max_length=255,
    )
    model: str = Field(
        description="Vehicle model name",
        max_length=255,
    )
    manufacturing_date: datetime = Field(
        description="Date when the vehicle was manufactured",
    )
    mileage: int = Field(
        description="Mileage of the vehicle in kilometers",
        ge=0,
    )
    engine: str = Field(
        description="Engine type or specification",
        max_length=255,
    )
    transmission: str = Field(
        description="Transmission type (e.g., automatic, manual)",
        max_length=255,
    )
    vin: str = Field(
        description="Vehicle Identification Number (VIN)",
        min_length=17,
        max_length=17,
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$",  # VIN format
    )
    images: list[HttpUrl] = Field(
        description="List of URLs to images of the vehicle",
        default_factory=list,
    )


class AuctionVehiclesQuery(PaginationParams):
    is_active: bool | None = Field(
        description="Filter vehicles by their active status",
        default=None,
    )
    model_ids: list[int] = Field(default_factory=list, description="Filter vehicles by a list of model IDs")
    manufacturer_ids: list[int] = Field(
        default_factory=list,
        description="Filter vehicles by a list of manufacturer IDs",
    )
    registration_year_from: int | None = Field(
        None,
        description="Filter vehicles manufactured from this year (inclusive)",
        ge=2000,
        le=datetime.now().year,
    )
    registration_year_to: int | None = Field(
        None,
        description="Filter vehicles manufactured up to this year (inclusive)",
        ge=2000,
        le=datetime.now().year,
    )
    mileage_from: int | None = Field(
        None,
        description="Filter vehicles with mileage from this value (inclusive)",
        ge=0,
    )
    mileage_to: int | None = Field(
        None,
        description="Filter vehicles with mileage up to this value (inclusive)",
        ge=0,
    )


class AuctionVehicleFacet(BaseModel):
    id: int | None = Field(
        description="Unique identifier for the facet (e.g., manufacturer or model ID)",
        ge=1,
    )
    name: str = Field(
        description="Name of the facet (e.g., manufacturer or model name)",
        max_length=255,
    )
    count: int = Field(
        description="Count of vehicles associated with this facet",
        ge=0,
    )


class AuctionVehicleFacets(BaseModel):
    manufacturers: list[AuctionVehicleFacet] = Field(
        description="Mapping of manufacturer names to the count of vehicles available from each manufacturer",
    )
    models: list[AuctionVehicleFacet] = Field(
        description="Mapping of model names to the count of vehicles available for each model",
    )
    registration_years: list[AuctionVehicleFacet] = Field(
        description="Mapping of registration years to the count of vehicles registered in each year",
    )


class AuctionVehicleUpdateRequest(BaseModel):
    is_active: bool | None = Field(None, description="Indicates if the vehicle is currently active in the auction")
    manufacturer_id: int | None = Field(None, description="Vehicle manufacturer id")
    model_id: int | None = Field(None, description="Vehicle model id")
    manufacturing_date: datetime | None = Field(None, description="Date when the vehicle was manufactured")
    mileage: int | None = Field(None, description="Mileage of the vehicle in kilometers")
    engine: str | None = Field(None, description="Engine type or specification")
    transmission: str | None = Field(None, description="Transmission type (e.g., automatic, manual)")
    vin: str | None = Field(None, description="Vehicle Identification Number (VIN)", min_length=17, max_length=17)


class AuctionVehiclesResponse(PaginatedResponse):
    items: list[AuctionVehicle] = Field(
        description="List of auction vehicles",
    )
    facets: AuctionVehicleFacets = Field(
        description="Facets for filtering auction vehicles",
    )


class AuctionVehicleResponse(BaseModel):
    vehicle: AuctionVehicle = Field(
        description="Details of the auction vehicle",
    )
