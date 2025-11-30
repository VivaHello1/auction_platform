from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped

from database.schema_base import ModelDeclarativeBase


class Auction(ModelDeclarativeBase):
    __tablename__ = "auctions"

    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[String] = Column(String(255), nullable=False)
    type: Mapped[String] = Column(String(255), nullable=False)
    leasing_company_id: Mapped[Integer | None] = Column(Integer, nullable=True)
    reference_url: Mapped[String | None] = Column(String(2048), nullable=True)
    country: Mapped[String] = Column(String(2), nullable=False)
    end_datetime: Mapped[DateTime] = Column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
