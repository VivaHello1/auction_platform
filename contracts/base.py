from pydantic import BaseModel, ConfigDict, Field


class PaginationParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)

    from_: int | None = Field(0, alias="from")
    size: int | None = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    total: int
