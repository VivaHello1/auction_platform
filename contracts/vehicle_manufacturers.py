from datetime import datetime

from pydantic import BaseModel, Field


class VehicleManufacturer(BaseModel):
    id: int = Field(..., description="Unique identifier for the vehicle manufacturer")
    name: str = Field(..., description="Name of the vehicle manufacturer")
    synonyms: list[str] = Field(default_factory=list, description="List of synonyms for the manufacturer")
    created_at: datetime = Field(..., description="Timestamp when the manufacturer was created")


class VehicleModel(BaseModel):
    id: int = Field(..., description="Unique identifier for the vehicle model")
    name: str = Field(..., description="Name of the vehicle model")
    default_vehicle_type: str = Field(..., description="Default vehicle type for the model (e.g., suv, sedan...)")
    synonyms: list[str] = Field(default_factory=list, description="List of synonyms for the vehicle model")
    created_at: datetime = Field(..., description="Timestamp when the model was created")


class VehicleManufacturersResponse(BaseModel):
    manufacturers: list[VehicleManufacturer] = Field(
        ...,
        description="List of vehicle manufacturers",
    )


class VehicleManufacturerResponse(BaseModel):
    manufacturer: VehicleManufacturer = Field(..., description="Details of the vehicle manufacturer")


class VehicleManufacturerRequest(BaseModel):
    name: str | None = Field(None, description="Name of the vehicle manufacturer")
    synonyms: list[str] | None = Field(None, description="List of synonyms for the manufacturer")


class VehicleModelRequest(BaseModel):
    name: str | None = Field(None, description="Name of the vehicle model")
    default_vehicle_type: str | None = Field(
        None, description="Default vehicle type for the model (e.g., suv, sedan...)"
    )
    synonyms: list[str] | None = Field(None, description="List of synonyms for the vehicle model")


class VehicleModelsResponse(BaseModel):
    manufacturer: VehicleManufacturer = Field(..., description="Details of the vehicle manufacturer")
    models: list[VehicleModel] = Field(default_factory=list, description="List of vehicle models for the manufacturer")


class VehicleModelResponse(BaseModel):
    model: VehicleModel = Field(..., description="Details of the vehicle model")
    manufacturer: VehicleManufacturer = Field(..., description="Details of the vehicle manufacturer")
