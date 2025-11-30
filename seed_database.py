#!/usr/bin/env python3
"""
Database seeding script for AutoBid API

This script populates the database with sample data for development and testing purposes.
It includes realistic data for users, auctions, vehicles, manufacturers, models.

Usage:
    python seed_database.py                    # Default: 20 users, 10 auctions, 8 vehicles
    python seed_database.py --auctions 20      # 20 users, 20 auctions, 8 vehicles
    python seed_database.py --vehicles 50      # 20 users, 10 auctions, 50 vehicles
    python seed_database.py --users 50 --auctions 15 --vehicles 100 --bids 50

Options:
    --users     Number of users to generate (default: 20)
    --auctions  Number of auctions to generate (default: 10)
    --vehicles  Number of vehicles to generate (default: 8)
    --bids      Number of user bids to generate (default: 20)

Make sure to run this after the database migrations have been applied.
"""

import argparse
import asyncio
import os
import random
from datetime import date, datetime, timedelta

from sqlalchemy import select

from core.logging import logger
from database.database import Database
from database.init_database import async_database_url
from repositories.models import (
    Auction,
    AuctionVehicle,
    User,
    VehicleManufacturer,
    VehicleModel,
)


class DatabaseSeeder:
    def __init__(self, num_auctions: int = 10, num_vehicles: int = 8, num_users: int = 20):
        self.db = Database(async_database_url(), os.getenv("POSTGRES_SCHEMA"))
        self.num_auctions = num_auctions
        self.num_vehicles = num_vehicles
        self.num_users = num_users

    async def seed_all(self):
        """Seeds the database with all sample data."""
        try:
            logger.info(
                f"Successfully seeded database with {self.num_auctions} auctions, "
                f"{self.num_vehicles} vehicles, {self.num_users} users."
            )

            async with self.db.session_factory() as session:
                # Check if data already exists
                existing_manufacturers = await session.execute(select(VehicleManufacturer))
                if existing_manufacturers.scalars().first():
                    logger.info("Database already contains seeded data. Skipping seeding.")
                    return

                # Seed in correct order (due to foreign key dependencies)
                await self._seed_users(session)
                await self._seed_vehicle_manufacturers(session)
                await self._seed_vehicle_models(session)
                await self._seed_auctions(session)
                await self._seed_auction_vehicles(session)

                logger.info("Database seeding completed successfully!")

        except Exception as e:
            logger.error(f"Error during database seeding: {e}")
            raise

    async def _seed_users(self, session):
        """Seeds user data."""
        logger.info(f"Seeding {self.num_users} users...")

        # Sample data for realistic user generation
        first_names = [
            "Jonas",
            "Andrius",
            "Mindaugas",
            "Vytautas",
            "Tomas",
            "Darius",
            "Gintaras",
            "Rokas",
            "Mantas",
            "Lukas",
            "Anna",
            "Elena",
            "Ruta",
            "Ieva",
            "Kristina",
            "Greta",
            "Neringa",
            "Agne",
            "Laura",
            "Egle",
            "John",
            "Michael",
            "David",
            "Robert",
            "James",
            "William",
            "Richard",
            "Thomas",
            "Charles",
            "Daniel",
            "Sarah",
            "Jessica",
            "Jennifer",
            "Lisa",
            "Susan",
            "Karen",
            "Nancy",
            "Betty",
            "Helen",
            "Sandra",
        ]

        last_names = [
            "Petraitis",
            "Kazlauskas",
            "Jankauskas",
            "Stankevicius",
            "Vasiliauskas",
            "Zukauskas",
            "Butkus",
            "Paulauskas",
            "Urbonas",
            "Kucinskis",
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
            "Rodriguez",
            "Martinez",
            "Hernandez",
            "Lopez",
            "Gonzalez",
            "Wilson",
            "Anderson",
            "Thomas",
            "Taylor",
            "Moore",
        ]

        languages = ["en", "lt", "lv", "de", "ru", "pl"]
        statuses = ["active", "inactive", "pending", "suspended"]
        countries = ["Lithuania", "Latvia", "Germany", "United Kingdom", "Poland", "Estonia"]

        users = []

        # Create some supervisor users first (top 20% will be supervisors)
        supervisor_count = max(1, self.num_users // 5)

        for i in range(self.num_users):
            first_name = first_names[i % len(first_names)]
            last_name = last_names[(i + 7) % len(last_names)]  # Offset to mix combinations

            # Generate realistic email
            email_variants = [
                f"{first_name.lower()}.{last_name.lower()}@example.com",
                f"{first_name.lower()}{i+1}@email.com",
                f"{last_name.lower()}.{first_name.lower()}@test.org",
            ]
            email = email_variants[i % len(email_variants)]

            # Phone number generation
            phone_prefixes = ["+370", "+371", "+49", "+44", "+48", "+372"]
            phone = f"{phone_prefixes[i % len(phone_prefixes)]}{random.randint(600000000, 699999999)}"

            # Passport number generation (realistic format)
            passport_formats = ["LT", "LV", "DE", "UK", "PL", "EE"]
            passport_country = passport_formats[i % len(passport_formats)]
            passport_number = f"{passport_country}{random.randint(1000000, 9999999)}"

            # Address generation
            street_names = [
                "Main St",
                "Oak Ave",
                "Park Rd",
                "Church St",
                "High St",
                "School Rd",
                "King St",
                "Queen Ave",
            ]
            cities = ["Vilnius", "Kaunas", "Klaipeda", "Riga", "Berlin", "London", "Warsaw", "Tallinn"]
            street = street_names[i % len(street_names)]
            city = cities[i % len(cities)]
            country = countries[i % len(countries)]
            address = f"{random.randint(1, 999)} {street}, {city}, {country}"

            # Generate registration date (last 2 years)
            days_ago = random.randint(1, 730)  # 1-730 days ago
            registration_date = datetime.now() - timedelta(days=days_ago)

            # Comments array
            comment_options = [
                ["New user", "Email verified"],
                ["Premium customer", "High value transactions"],
                ["Regular customer", "Reliable payments"],
                ["Corporate account", "Fleet purchases"],
                ["VIP member", "Priority support"],
                ["First time buyer", "Needs assistance"],
                [],  # Some users have no comments
            ]
            comments = comment_options[i % len(comment_options)]

            user = User(
                supervisor_id=None,  # Will be set after supervisors are created
                phone_number=phone,
                passport_number=passport_number,
                address=address,
                language=languages[i % len(languages)],
                email=email,
                registration_date=registration_date,
                comments=comments if comments else None,
                status=statuses[i % len(statuses)],
            )
            users.append(user)

        # Add all users first
        for user in users:
            session.add(user)

        await session.flush()

        # Now assign supervisors using the actual UUIDs
        for i in range(len(users)):
            if i >= supervisor_count:  # Non-supervisor users get supervisors
                supervisor_idx = i % supervisor_count
                users[i].supervisor_id = users[supervisor_idx].id

        await session.flush()
        logger.info(f"Added {len(users)} users ({supervisor_count} supervisors)")

    async def _seed_vehicle_manufacturers(self, session):
        """Seeds vehicle manufacturers data."""
        logger.info("Seeding vehicle manufacturers...")

        manufacturers = [
            VehicleManufacturer(name="BMW", synonyms=["Bayerische Motoren Werke", "Bavarian Motor Works"]),
            VehicleManufacturer(name="Mercedes-Benz", synonyms=["Mercedes", "Benz", "Daimler"]),
            VehicleManufacturer(name="Audi", synonyms=["Audi AG"]),
            VehicleManufacturer(name="Volkswagen", synonyms=["VW", "Volkswagen AG", "Volks"]),
            VehicleManufacturer(name="Toyota", synonyms=["Toyota Motor Corporation"]),
            VehicleManufacturer(name="Honda", synonyms=["Honda Motor Co"]),
            VehicleManufacturer(name="Ford", synonyms=["Ford Motor Company"]),
            VehicleManufacturer(name="Opel", synonyms=["Opel AG", "Vauxhall"]),
            VehicleManufacturer(name="Peugeot", synonyms=["Peugeot SA"]),
            VehicleManufacturer(name="Renault", synonyms=["Renault SA"]),
        ]

        for manufacturer in manufacturers:
            session.add(manufacturer)

        await session.flush()
        logger.info(f"Added {len(manufacturers)} vehicle manufacturers")

    async def _seed_vehicle_models(self, session):
        """Seeds vehicle models data."""
        logger.info("Seeding vehicle models...")

        # Get manufacturer IDs from the database
        manufacturer_result = await session.execute(select(VehicleManufacturer))
        manufacturers = {m.name: m.id for m in manufacturer_result.scalars().all()}

        models = [
            # BMW Models
            VehicleModel(
                manufacturer_id=manufacturers["BMW"],
                name="3 Series",
                default_vehicle_type="sedan",
                synonyms=["320i", "330i", "335i"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["BMW"],
                name="5 Series",
                default_vehicle_type="sedan",
                synonyms=["520i", "530i", "540i"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["BMW"], name="X3", default_vehicle_type="suv", synonyms=["BMW X3"]
            ),
            VehicleModel(
                manufacturer_id=manufacturers["BMW"], name="X5", default_vehicle_type="suv", synonyms=["BMW X5"]
            ),
            # Mercedes-Benz Models
            VehicleModel(
                manufacturer_id=manufacturers["Mercedes-Benz"],
                name="C-Class",
                default_vehicle_type="sedan",
                synonyms=["C200", "C220", "C250"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Mercedes-Benz"],
                name="E-Class",
                default_vehicle_type="sedan",
                synonyms=["E200", "E220", "E250"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Mercedes-Benz"],
                name="GLC",
                default_vehicle_type="suv",
                synonyms=["GLC 200", "GLC 220"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Mercedes-Benz"],
                name="A-Class",
                default_vehicle_type="hatchback",
                synonyms=["A180", "A200", "A220"],
            ),
            # Audi Models
            VehicleModel(
                manufacturer_id=manufacturers["Audi"], name="A3", default_vehicle_type="hatchback", synonyms=["Audi A3"]
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Audi"], name="A4", default_vehicle_type="sedan", synonyms=["Audi A4"]
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Audi"], name="Q3", default_vehicle_type="suv", synonyms=["Audi Q3"]
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Audi"], name="Q5", default_vehicle_type="suv", synonyms=["Audi Q5"]
            ),
            # Volkswagen Models
            VehicleModel(
                manufacturer_id=manufacturers["Volkswagen"],
                name="Golf",
                default_vehicle_type="hatchback",
                synonyms=["VW Golf", "Golf GTI"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Volkswagen"],
                name="Passat",
                default_vehicle_type="sedan",
                synonyms=["VW Passat"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Volkswagen"],
                name="Tiguan",
                default_vehicle_type="suv",
                synonyms=["VW Tiguan"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Volkswagen"],
                name="Polo",
                default_vehicle_type="hatchback",
                synonyms=["VW Polo"],
            ),
            # Toyota Models
            VehicleModel(
                manufacturer_id=manufacturers["Toyota"],
                name="Corolla",
                default_vehicle_type="sedan",
                synonyms=["Toyota Corolla"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Toyota"],
                name="Camry",
                default_vehicle_type="sedan",
                synonyms=["Toyota Camry"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Toyota"],
                name="RAV4",
                default_vehicle_type="suv",
                synonyms=["Toyota RAV4"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Toyota"],
                name="Prius",
                default_vehicle_type="hybrid",
                synonyms=["Toyota Prius"],
            ),
            # Honda Models
            VehicleModel(
                manufacturer_id=manufacturers["Honda"],
                name="Civic",
                default_vehicle_type="sedan",
                synonyms=["Honda Civic"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Honda"],
                name="Accord",
                default_vehicle_type="sedan",
                synonyms=["Honda Accord"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Honda"], name="CR-V", default_vehicle_type="suv", synonyms=["Honda CR-V"]
            ),
            # Ford Models
            VehicleModel(
                manufacturer_id=manufacturers["Ford"],
                name="Focus",
                default_vehicle_type="hatchback",
                synonyms=["Ford Focus"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Ford"],
                name="Mondeo",
                default_vehicle_type="sedan",
                synonyms=["Ford Mondeo"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Ford"], name="Kuga", default_vehicle_type="suv", synonyms=["Ford Kuga"]
            ),
            # Opel Models
            VehicleModel(
                manufacturer_id=manufacturers["Opel"],
                name="Astra",
                default_vehicle_type="hatchback",
                synonyms=["Opel Astra"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Opel"],
                name="Insignia",
                default_vehicle_type="sedan",
                synonyms=["Opel Insignia"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Opel"], name="Mokka", default_vehicle_type="suv", synonyms=["Opel Mokka"]
            ),
            # Peugeot Models
            VehicleModel(
                manufacturer_id=manufacturers["Peugeot"],
                name="308",
                default_vehicle_type="hatchback",
                synonyms=["Peugeot 308"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Peugeot"],
                name="508",
                default_vehicle_type="sedan",
                synonyms=["Peugeot 508"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Peugeot"],
                name="3008",
                default_vehicle_type="suv",
                synonyms=["Peugeot 3008"],
            ),
            # Renault Models
            VehicleModel(
                manufacturer_id=manufacturers["Renault"],
                name="Clio",
                default_vehicle_type="hatchback",
                synonyms=["Renault Clio"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Renault"],
                name="Megane",
                default_vehicle_type="hatchback",
                synonyms=["Renault Megane"],
            ),
            VehicleModel(
                manufacturer_id=manufacturers["Renault"],
                name="Kadjar",
                default_vehicle_type="suv",
                synonyms=["Renault Kadjar"],
            ),
        ]

        for model in models:
            session.add(model)

        await session.flush()
        logger.info(f"Added {len(models)} vehicle models")

    async def _seed_auctions(self, session):
        """Seeds auction data."""
        logger.info(f"Seeding {self.num_auctions} auctions...")

        # Generate auctions with various end dates (some past, some future)
        base_date = datetime.now()

        # Auction types and countries to cycle through
        auction_types = ["fleet", "premium", "executive", "commercial", "luxury", "general", "festival", "electric"]
        countries = ["DE", "GB", "FR", "NL", "IT", "ES", "SE", "NO", "AT", "BE"]

        auctions = []

        for i in range(self.num_auctions):
            auction_id = 10001 + i
            auction_type = auction_types[i % len(auction_types)]
            country = countries[i % len(countries)]

            # Vary end dates: some past, mostly future
            if i < self.num_auctions // 4:  # 25% past auctions
                end_date = base_date - timedelta(days=(i + 1) * 2, hours=10 + i)
            else:  # 75% future auctions
                days_ahead = (i - self.num_auctions // 4 + 1) * 7  # Weekly spacing
                end_date = base_date + timedelta(days=days_ahead, hours=14 + (i % 8))

            auction = Auction(
                id=auction_id,
                name=f"{auction_type.title()} Auction {i + 1}",
                type=auction_type,
                reference_url=f"{auction_type.upper()[:3]}-2025-{auction_id:03d}",
                country=country,
                end_datetime=end_date,
            )
            auctions.append(auction)

        for auction in auctions:
            session.add(auction)

        await session.flush()
        logger.info(f"Added {len(auctions)} auctions")

    async def _seed_auction_vehicles(self, session):
        """Seeds vehicle data."""
        logger.info(f"Seeding {self.num_vehicles} vehicles...")

        # Get all auction IDs to distribute vehicles across them
        auction_result = await session.execute(select(Auction.id))
        auction_ids = [row[0] for row in auction_result.fetchall()]

        if not auction_ids:
            logger.warning("No auctions found, cannot seed vehicles")
            return

        # Get manufacturer and model IDs
        manufacturer_result = await session.execute(select(VehicleManufacturer))
        manufacturers = list(manufacturer_result.scalars().all())

        model_result = await session.execute(select(VehicleModel))
        models = list(model_result.scalars().all())

        if not manufacturers or not models:
            logger.warning("No manufacturers or models found, cannot seed vehicles")
            return

        # Vehicle data templates for generation
        vehicle_types = ["Sedan", "SUV", "Hatchback", "Hybrid", "Wagon", "Coupe"]
        colors = [
            "Jet Black",
            "Alpine White",
            "Obsidian Black",
            "Brilliant Black",
            "Tornado Red",
            "Super White",
            "Magnetic Grey",
            "Sovereign Silver",
            "Deep Blue",
            "Pearl White",
        ]
        transmissions = ["Automatic", "Manual", "S tronic", "CVT"]

        vehicles = []

        for i in range(self.num_vehicles):
            vehicle_id = i + 1000000  # Ensure unique vehicle IDs starting from 1,000,000
            auction_id = auction_ids[i % len(auction_ids)]  # Distribute across auctions
            manufacturer = manufacturers[random.randint(0, len(manufacturers) - 1)]  # Cycle through manufacturers
            model = models[i % len(models)]  # Cycle through models

            # Generate realistic manufacturing date (2014-2025)
            manufacturing_year = random.randint(2014, 2025)
            manufacturing_month = (i % 12) + 1
            manufacturing_day = min((i % 28) + 1, 28)  # Ensure valid day

            # Generate realistic vin
            vin = await self.generate_realistic_vin()

            # Generate realistic mileage based on age
            age_years = 2025 - manufacturing_year
            base_mileage = age_years * random.randint(5000, 15000)  # 15k miles per year average
            mileage_variation = (i * 1000) % 20000  # Add some variation
            mileage = base_mileage + mileage_variation

            # Generate prices
            base_price = 15000 + (i * 1000) % 40000  # Range from 15k to 55k

            # Some variety in vehicle status
            is_active = i >= self.num_vehicles // 4  # 75% active
            is_damaged = (i % 10) == 0  # 10% damaged

            # Generate random car images (3-5 images per vehicle)
            image_list = await self.generate_images(i)

            vehicle = AuctionVehicle(
                id=vehicle_id,
                auction_id=auction_id,
                manufacturer_id=manufacturer.id,
                model_id=model.id,
                manufacturing_date=date(manufacturing_year, manufacturing_month, manufacturing_day),
                mileage=mileage,
                engine=f"{1.0 + (i % 3) * 0.5:.1f}L {'Turbo' if i % 2 == 0 else 'Diesel'}",
                transmission=transmissions[i % len(transmissions)],
                vin=vin,
                body_type=f"{4 + (i % 2)}-door {vehicle_types[i % len(vehicle_types)].lower()}",
                color=colors[i % len(colors)],
                engine_power=120 + (i * 10) % 200,  # 120-320 HP
                engine_cc=1200 + (i * 100) % 2000,  # 1200-3200cc
                start_price=base_price,
                active=is_active,
                is_damaged=is_damaged,
                number_plates=f"GEN-{vehicle_id:04d}",
                equipment=[
                    "Navigation" if i % 3 == 0 else "Radio",
                    "Leather seats" if i % 4 == 0 else "Fabric seats",
                    "Air conditioning",
                    "Parking sensors" if i % 5 == 0 else "Manual parking",
                ],
                description=(
                    f"Generated vehicle {vehicle_id} - {vehicle_types[i % len(vehicle_types)]} in excellent condition."
                ),
                image_list=image_list,
            )
            vehicles.append(vehicle)

        for vehicle in vehicles:
            session.add(vehicle)

        await session.flush()
        logger.info(f"Added {len(vehicles)} vehicles")

    async def generate_realistic_vin(self) -> str:
        """Generate a more realistic VIN following standard structure"""
        valid_chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"

        # WMI (World Manufacturer Identifier) - 3 chars
        wmi = ''.join(random.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(3))

        # VDS (Vehicle Descriptor Section) - 6 chars
        vds = ''.join(random.choice(valid_chars) for _ in range(6))

        # VIS (Vehicle Identifier Section) - 8 chars
        vis = ''.join(random.choice(valid_chars) for _ in range(8))

        return wmi + vds + vis

    async def generate_images(self, index) -> list[str]:
        num_images = 3 + (index % 3)  # 3-5 images
        image_list = []
        for img_idx in range(num_images):
            car_image_ids = [
                111,
                183,
                193,
                305,
                306,
                309,
                310,
                311,
                312,
                313,
                378,
                379,
                380,
            ]

            # Select a random car image ID and add some randomness
            base_id = car_image_ids[(index + img_idx) % len(car_image_ids)]
            random_offset = (index * 7 + img_idx * 13) % 50  # Add some variation
            image_id = base_id + random_offset

            # Different image sizes for variety
            sizes = ["800/600", "600/400", "900/600", "700/500", "1000/700"]
            size = sizes[img_idx % len(sizes)]

            image_url = f"https://picsum.photos/id/{image_id}/{size}"
            image_list.append(image_url)

        return image_list

    async def cleanup(self):
        """Cleanup database connections."""
        await self.db.close_db()


async def main():
    """Main function to run the database seeding."""
    parser = argparse.ArgumentParser(description="Seed the database with sample data")
    parser.add_argument("--auctions", type=int, default=10, help="Number of auctions to generate (default: 10)")
    parser.add_argument("--vehicles", type=int, default=8, help="Number of vehicles to generate (default: 8)")
    parser.add_argument("--users", type=int, default=20, help="Number of users to generate (default: 20)")

    args = parser.parse_args()

    seeder = DatabaseSeeder(num_auctions=args.auctions, num_vehicles=args.vehicles, num_users=args.users)

    try:
        await seeder.seed_all()
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise
    finally:
        await seeder.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
