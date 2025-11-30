from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class ModelDeclarativeBase(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""


__all__ = [
    'ModelDeclarativeBase',
]
