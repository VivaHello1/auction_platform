import logging
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


def database_url():
    return (
        f"postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:"
        f"{quote_plus(os.getenv("POSTGRES_PASSWORD"))}@{os.getenv("POSTGRES_HOST")}:5432/"
        f"{os.getenv("POSTGRES_DB")}"
    )


def async_database_url():
    return (
        f"postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:"
        f"{quote_plus(os.getenv("POSTGRES_PASSWORD"))}@{os.getenv("POSTGRES_HOST")}:5432/"
        f"{os.getenv("POSTGRES_DB")}"
    )


def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    # Connect to postgres database to create our target database
    postgres_url = database_url()
    postgres_db = os.getenv("POSTGRES_DB")
    engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")

    try:
        with engine.connect() as connection:
            # Check if database exists
            result = connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"), {"db_name": postgres_db}
            )

            if not result.fetchone():
                logger.info(f"Creating database: {postgres_db}")
                connection.execute(text(f"CREATE DATABASE {postgres_db}"))
                logger.info(f"Database {postgres_db} created successfully")
            else:
                logger.info(f"Database {postgres_db} already exists")

    except OperationalError as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        engine.dispose()


def create_schema_if_not_exists():
    """Create the schema if it doesn't exist."""
    postgres_url = database_url()
    postgres_schema = os.getenv("POSTGRES_SCHEMA")
    if not postgres_schema:
        return

    engine = create_engine(postgres_url)

    try:
        with engine.connect() as connection:
            logger.info(f"Creating schema: {postgres_schema}")
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {postgres_schema}"))
            connection.commit()
            logger.info(f"Schema {postgres_schema} ready")
    except OperationalError as e:
        logger.error(f"Error creating schema: {e}")
        raise
    finally:
        engine.dispose()


def initialize_database():
    """Initialize database and schema."""
    create_database_if_not_exists()
    create_schema_if_not_exists()
