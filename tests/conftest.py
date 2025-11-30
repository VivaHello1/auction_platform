import pytest
import sqlalchemy

from tests import test_container, test_settings


def pytest_collection_modifyitems(items):
    """Modifies test items in place to ensure critical tests run first."""
    critical_module_prefix = "tests.critical"
    module_mapping = {item: item.module.__name__ for item in items}

    critical_items = [item for item in items if module_mapping[item].startswith(critical_module_prefix)]
    other_items = [item for item in items if not module_mapping[item].startswith(critical_module_prefix)]

    items[:] = critical_items + other_items


@pytest.fixture(scope="package")
def container():
    test_container.init_resources()
    yield test_container
    test_container.shutdown_resources()


@pytest.fixture(scope="package")
async def database_create_destroy(container):
    db = container.db()

    await db.init_db()

    yield db

    session = db.sync_session()
    try:
        inspector = sqlalchemy.inspect(db.engine)
        for table_name in inspector.get_table_names(schema=test_settings.POSTGRES_SCHEMA):
            table_ref = f"{test_settings.POSTGRES_SCHEMA}.{table_name}"
            session.execute(sqlalchemy.text(f"DROP TABLE IF EXISTS {table_ref} CASCADE"))
        session.commit()
    finally:
        session.close()

    await db.close_db()


@pytest.fixture(scope="function")
def clean_db(database_create_destroy):
    db = database_create_destroy

    session = db.sync_session()
    try:
        inspector = sqlalchemy.inspect(db.engine)
        schema_tables = inspector.get_table_names(schema=test_settings.POSTGRES_SCHEMA)

        for table_name in schema_tables:
            table_ref = f"{test_settings.POSTGRES_SCHEMA}.{table_name}"
            session.execute(sqlalchemy.text(f"TRUNCATE {table_ref} CASCADE"))

        session.commit()
    finally:
        session.close()

    return db
