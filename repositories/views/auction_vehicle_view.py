from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AuctionVehicleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    auction_id: int
    active: bool
    manufacturing_date: datetime
    type: str | None
    mileage: int
    engine: str
    transmission: str
    vin: str
    image_list: list[HttpUrl] = Field(default_factory=list)


class VehicleManufacturerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class VehicleModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class FacetView(BaseModel):
    """View for facet data with id, name, and count"""

    model_config = ConfigDict(from_attributes=True)

    id: int | None
    name: str
    count: int


class AuctionVehicleView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vehicle: AuctionVehicleSchema
    manufacturer: VehicleManufacturerSchema
    model: VehicleModelSchema
