from datetime import datetime

from pydantic import BaseModel, Field

from .base import PaginatedResponse, PaginationParams


class AuctionCarPreview(BaseModel):
    id: int = Field(
        description="Unique identifier for the car",
        ge=1000000,  # Assuming car IDs start from 1,000,000
    )
    manufacturer_id: int = Field(
        description="Unique identifier for the manufacturer",
        ge=1,
    )
    manufacturer: str = Field(
        description="Manufacturer of the car",
        min_length=1,
        max_length=50,
    )
    model_id: int = Field(
        description="Unique identifier for the model",
        ge=1,
    )
    model: str = Field(
        description="Model of the car",
        min_length=1,
        max_length=50,
    )
    mileage: int = Field(
        description="Mileage of the car in kilometers",
        ge=0,
    )
    manufacturing_date: datetime = Field(
        description="Manufacturing date of the car",
    )


class Auction(BaseModel):
    id: int = Field(
        description="Unique identifier for the auction",
        ge=10000,  # Assuming auction IDs start from 10000
    )
    country: str = Field(
        description="Country code where the auction is held",
        min_length=2,
        max_length=2,
    )  # ISO 3166-1 alpha-2 (e.g., "US", "GB", "DE")
    name: str = Field(
        description="Title of the auction",
        min_length=1,
        max_length=100,
    )
    car_count: int = Field(
        description="Number of cars available in the auction",
        ge=0,
    )
    close_date: datetime = Field(
        description="Date and time when the auction closes",
    )
    status: str = Field(
        description="Current status of the auction",
        pattern=r"^(active|closed|)$",
    )
    car_preview: list[AuctionCarPreview] = Field(
        description="List of car previews in the auction",
        default_factory=list,
    )


class AuctionResponse(BaseModel):
    auction: Auction = Field(
        description="Details of the auction",
    )


class AuctionsListResponse(PaginatedResponse):
    items: list[Auction] = Field(
        description="List of auctions",
    )


class AuctionsListQuery(PaginationParams):
    country: str | None = Field(
        description="Country code to filter auctions by (ISO 3166-1 alpha-2)",
        default=None,
        min_length=2,
        max_length=2,
    )
    status: str | None = Field(
        description="Status of the auctions to filter by",
        default=None,
        pattern=r"^(active|closed|)$",
    )
