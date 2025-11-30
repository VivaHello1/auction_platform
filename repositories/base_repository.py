from collections.abc import AsyncGenerator, Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select


class BaseRepository:
    def __init__(self, session_factory: Callable[[], AsyncGenerator[AsyncSession, None]]):
        self.session_factory = session_factory

    async def commit_session(self) -> None:
        async for session in self.get_db_session():
            await session.commit()
            await session.close()

    def _apply_filters(self, query: Select, filters: dict, model: DeclarativeMeta) -> Select:
        """
        Apply filters to a query based on the provided model and filters dictionary.

        Supports range filtering with operators:
        - field__gte: Greater than or equal
        - field__lte: Less than or equal
        - field__gt: Greater than
        - field__lt: Less than
        - field__between: Between two values (expects list/tuple with 2 values)

        :param query: The SQLAlchemy query to modify.
        :param filters: A dictionary of filters to apply.
        :param model: The SQLAlchemy model to filter on.
        :return: The modified query with filters applied.
        """
        range_operators = {
            '__gte': lambda field, val: field >= val,
            '__lte': lambda field, val: field <= val,
            '__gt': lambda field, val: field > val,
            '__lt': lambda field, val: field < val,
            '__between': lambda field, val: (
                field.between(val[0], val[1]) if isinstance(val, list | tuple) and len(val) == 2 else None
            ),
        }

        for key, value in filters.items():
            if value is None:
                continue

            # Check for range operators
            range_applied = False
            for operator, filter_func in range_operators.items():
                if key.endswith(operator):
                    field_name = key[: len(operator) * -1]
                    if hasattr(model, field_name):
                        condition = filter_func(getattr(model, field_name), value)
                        if condition is not None:
                            query = query.filter(condition)
                        range_applied = True
                    break

            # Apply original equality/in logic if no range operator was used
            if not range_applied and hasattr(model, key):
                if isinstance(value, list):
                    query = query.filter(getattr(model, key).in_(value))
                else:
                    query = query.filter(getattr(model, key) == value)
        return query

    async def get_column_facets(self, column: InstrumentedAttribute, model: DeclarativeMeta, **kwargs) -> dict:
        """
        Get facet counts for a specific column with optional filters applied.

        :param column: SQLAlchemy column to get facets for
        :param model: SQLAlchemy model to apply filters on
        :param kwargs: Filter dictionary to apply
        :return: Dictionary mapping column values to their counts
        """
        if not isinstance(column, InstrumentedAttribute):
            raise ValueError("column must be a valid SQLAlchemy column (InstrumentedAttribute).")

        query = select(column, func.count().label("count")).group_by(column)
        query = self._apply_filters(query, kwargs, model)

        async with self.session_factory() as session:
            result = await session.execute(query)

        facets = {}
        for row in result:
            facets[row[0]] = row.count

        return facets
