from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped

from database.schema_base import ModelDeclarativeBase


class VehicleManufacturer(ModelDeclarativeBase):
    __tablename__ = "vehicle_manufacturers"

    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[String] = Column(String(255), nullable=False, unique=True)
    synonyms: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
