from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped

from database.schema_base import ModelDeclarativeBase


class VehicleModel(ModelDeclarativeBase):
    __tablename__ = "vehicle_models"

    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[Integer] = Column(Integer, nullable=False)
    name: Mapped[String] = Column(String(255), nullable=False)
    default_vehicle_type: Mapped[String] = Column(
        String(50), nullable=False, comment="Default vehicle type for the model (e.g., suv, sedan...)"
    )
    synonyms: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
