from datetime import date

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped

from database.schema_base import ModelDeclarativeBase


class AuctionVehicle(ModelDeclarativeBase):
    __tablename__ = "auction_vehicles"

    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=False)
    auction_id: Mapped[Integer] = Column(Integer, nullable=False)
    manufacturer_id: Mapped[Integer] = Column(Integer, nullable=False)
    model_id: Mapped[Integer] = Column(Integer, nullable=False)
    manufacturing_date: Mapped[date] = Column(Date, nullable=False)
    mileage: Mapped[Integer] = Column(Integer, nullable=False)
    engine: Mapped[String] = Column(String(255), nullable=False)  # Fuel type
    transmission: Mapped[String] = Column(String(255), nullable=False)
    vin: Mapped[String] = Column(String(17), nullable=False, unique=True)
    body_type: Mapped[String] = Column(String(255), nullable=True)
    color: Mapped[String] = Column(String(255), nullable=True)
    engine_power: Mapped[Integer] = Column(Integer, nullable=False)
    engine_cc: Mapped[Integer] = Column(Integer, nullable=False)
    start_price: Mapped[Integer] = Column(Integer, nullable=False)
    active: Mapped[bool] = Column(Boolean, nullable=False, default=True)
    is_damaged: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    number_plates: Mapped[String] = Column(String(20), nullable=True)
    equipment: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)  # Extra things like steering wheel heating
    description: Mapped[String] = Column(Text, nullable=True)
    image_list: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)
    damaged_image_list: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
