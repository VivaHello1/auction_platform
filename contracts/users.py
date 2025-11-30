from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(description="Unique identifier for the user")
    supervisor_id: int | None = Field(
        description="ID of the user's supervisor",
        default=None,
    )
    phone_number: str | None = Field(
        description="User's phone number",
        default=None,
        max_length=20,
    )
    passport_number: str | None = Field(
        description="User's passport number",
        default=None,
        max_length=50,
    )
    address: str | None = Field(
        description="User's address",
        default=None,
    )
    language: str = Field(
        description="User's preferred language",
        max_length=10,
        default="en",
    )
    email: str = Field(
        description="User's email address",
        max_length=255,
    )
    registration_date: datetime = Field(
        description="Date when the user registered",
    )
    comments: list[str] | None = Field(
        description="Comments about the user",
        default=None,
    )
    status: str = Field(
        description="User's account status",
        max_length=50,
        default="active",
    )


class UserRegistrationResponse(BaseModel):
    user: User = Field(description="User details")


class UserRegistrationUpdateRequest(BaseModel):
    supervisor_id: int | None = Field(
        description="ID of the user's supervisor",
        default=None,
    )
    phone_number: str | None = Field(
        description="User's phone number",
        default=None,
        max_length=20,
    )
    passport_number: str | None = Field(
        description="User's passport number",
        default=None,
        max_length=50,
    )
    address: str | None = Field(
        description="User's address",
        default=None,
    )
    language: str | None = Field(
        description="User's preferred language",
        default=None,
        max_length=10,
    )
    email: str | None = Field(
        description="User's email address",
        default=None,
        max_length=255,
    )
    status: str | None = Field(
        description="User's account status",
        default=None,
        max_length=50,
    )
