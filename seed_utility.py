#!/usr/bin/env python3
"""
Simple database seeding utility script

This script provides a convenient way to seed the database with sample data.
It can also be used to clear existing data if needed.

Usage:
    python seed_utility.py --seed                              # Seed with defaults (10 auctions, 8 vehicles, 20 bids)
    python seed_utility.py --seed --auctions 20                # Seed with 20 auctions, 8 vehicles, 20 bids
    python seed_utility.py --seed --vehicles 50                # Seed with 10 auctions, 50 vehicles, 20 bids
    python seed_utility.py --seed --auctions 15 --vehicles 100 --bids 50 # Seed with 15 auctions, 100 vehicles, 50 bids
    python seed_utility.py --clear                             # Clear all data
    python seed_utility.py --reset --auctions 5 --vehicles 20  # Clear and then seed with custom amounts

Options:
    --seed      Seed the database with sample data
    --clear     Clear all data from the database
    --reset     Clear and then seed the database
    --auctions  Number of auctions to generate (default: 10)
    --vehicles  Number of vehicles to generate (default: 8)
"""

import argparse
import asyncio
import os

from sqlalchemy import text

from core.logging import logger
from database.database import Database
from database.init_database import async_database_url
from seed_database import DatabaseSeeder


class SeedUtility:
    def __init__(self, num_auctions: int = 10, num_vehicles: int = 8, num_bids: int = 20):
        self.postgres_schema = os.getenv("POSTGRES_SCHEMA")
        self.db = Database(async_database_url(), self.postgres_schema)
        self.seeder = DatabaseSeeder(num_auctions=num_auctions, num_vehicles=num_vehicles)

    async def clear_database(self):
        """Clears all data from the database tables."""
        logger.info("Clearing database...")

        async with self.db.session_factory() as session:
            # Clear in reverse order of dependencies
            tables = [
                'auction_vehicles',
                'auctions',
                'users',
                'vehicle_models',
                'vehicle_manufacturers',
                'leasing_companies',
            ]

            for table in tables:
                try:
                    await session.execute(
                        text(f"TRUNCATE TABLE {self.postgres_schema}.{table} RESTART IDENTITY CASCADE")
                    )
                    logger.info(f"Cleared table: {table}")
                except Exception as e:
                    logger.warning(f"Could not clear table {table}: {e}")

        logger.info("Database cleared successfully!")

    async def seed_database(self):
        """Seeds the database with sample data."""
        await self.seeder.seed_all()

    async def reset_database(self):
        """Clears and then seeds the database."""
        await self.clear_database()
        await self.seed_database()

    async def cleanup(self):
        """Cleanup database connections."""
        await self.db.close_db()
        await self.seeder.cleanup()


async def main():
    parser = argparse.ArgumentParser(description='Database seeding utility')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--seed', action='store_true', help='Seed the database with sample data')
    group.add_argument('--clear', action='store_true', help='Clear all data from the database')
    group.add_argument('--reset', action='store_true', help='Clear and then seed the database')

    # Add optional parameters for seeding
    parser.add_argument(
        '--auctions', type=int, default=10, help='Number of auctions to generate when seeding (default: 10)'
    )
    parser.add_argument(
        '--vehicles', type=int, default=8, help='Number of vehicles to generate when seeding (default: 8)'
    )
    parser.add_argument(
        '--bids', type=int, default=20, help='Number of user bids to generate when seeding (default: 20)'
    )

    args = parser.parse_args()

    utility = SeedUtility(num_auctions=args.auctions, num_vehicles=args.vehicles, num_bids=args.bids)

    try:
        if args.seed:
            await utility.seed_database()
        elif args.clear:
            await utility.clear_database()
        elif args.reset:
            await utility.reset_database()

        logger.info("Operation completed successfully!")

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise
    finally:
        await utility.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
