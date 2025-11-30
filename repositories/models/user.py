import uuid
from uuid import uuid4

from sqlalchemy import ARRAY, UUID, Column, DateTime, String, Text, func
from sqlalchemy.orm import Mapped

from database.schema_base import ModelDeclarativeBase


class User(ModelDeclarativeBase):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4())
    supervisor_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), nullable=True)
    phone_number: Mapped[String] = Column(String(20), nullable=True)
    passport_number: Mapped[String] = Column(String(50), nullable=True, unique=True)
    address: Mapped[Text] = Column(Text, nullable=True)
    language: Mapped[String] = Column(String(10), nullable=False, server_default="en")
    email: Mapped[String] = Column(String(255), nullable=True, unique=True)
    registration_date: Mapped[DateTime] = Column(DateTime(timezone=True), nullable=False)
    comments: Mapped[ARRAY[String]] = Column(ARRAY(String), nullable=True)
    status: Mapped[String] = Column(String(50), nullable=False, server_default="unverified")
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
