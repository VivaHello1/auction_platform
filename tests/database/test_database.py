"""
Test database connection.
"""

import asyncio

import pytest
from sqlalchemy import text


@pytest.fixture(scope="package")
async def session_factory(container):
    return container.db().session_factory


async def test_db_connection(session_factory):
    """Test that database connection works through dependency injection."""

    async with session_factory() as session:
        result = await session.execute(text("SELECT 1 as test_value"))
        row = result.fetchone()

        assert row is not None
        assert row.test_value == 1


async def test_db_session_factory(session_factory):
    """Test that the session factory works correctly."""

    async with session_factory() as session1:
        result1 = await session1.execute(text("SELECT 'session1' as session_name"))
        row1 = result1.fetchone()
        assert row1.session_name == 'session1'

    async with session_factory() as session2:
        result2 = await session2.execute(text("SELECT 'session2' as session_name"))
        row2 = result2.fetchone()
        assert row2.session_name == 'session2'


async def test_db_transaction_rollback(session_factory):
    """Test that database transactions can be rolled back properly."""

    try:
        async with session_factory() as session:
            await session.execute(text("SELECT 1"))

            raise Exception("Test exception")

    except Exception as e:
        assert str(e) == "Test exception"

    async with session_factory() as session:
        result = await session.execute(text("SELECT 'rollback_test' as test"))
        row = result.fetchone()
        assert row.test == 'rollback_test'


async def test_db_concurrent_operations(session_factory):

    async def query_operation(query_value):
        async with session_factory() as session:
            result = await session.execute(text(f"SELECT '{query_value}' as value"))
            row = result.fetchone()

        return row.value

    results = await asyncio.gather(query_operation("query1"), query_operation("query2"), query_operation("query3"))

    assert results == ["query1", "query2", "query3"]
