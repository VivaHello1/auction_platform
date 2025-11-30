# Vehicle Auction Platform API

A modern, production-ready FastAPI backend for managing vehicle auctions. Built with PostgreSQL, SQLAlchemy, and async Python for high performance.

## Features

- **RESTful API** - Clean API design with FastAPI and Pydantic validation
- **Async/Await** - Fully asynchronous database operations for optimal performance
- **Database Migrations** - Alembic for reliable schema versioning
- **Type Safety** - Comprehensive type hints throughout the codebase
- **Dependency Injection** - Clean architecture with dependency-injector
- **Testing** - Comprehensive test suite with pytest
- **Code Quality** - Automated formatting and linting with Black, isort, and Ruff

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Testing**: pytest
- **Code Quality**: Black, isort, Ruff
- **Containerization**: Docker & Docker Compose

## Project Structure

```
.
├── alembic/              # Database migrations
├── contracts/            # Pydantic models for API validation
├── controllers/          # FastAPI routers and endpoints
│   └── v1/              # API v1 controllers
├── core/                # Core application configuration
├── database/            # Database setup and initialization
├── mappers/             # Data transformation layer
├── middlewares/         # Custom FastAPI middleware
├── repositories/        # Data access layer
│   └── models/          # SQLAlchemy models
├── services/            # Business logic layer
└── tests/               # Test suite
    ├── critical/        # Critical integration tests
    ├── factories/       # Test data factories
    ├── repositories/    # Repository tests
    └── services/        # Service tests
```

## Quick Start

### Prerequisites

- Python 3.13+
- Poetry
- Docker & Docker Compose
- Task (optional, for task runner)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auction_platform
   ```

2. **Install dependencies**
   ```bash
   poetry install --no-root
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.development
   ```

   Update `.env.development` with your configuration:
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_DB=auction_development
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_SCHEMA=api
   ENVIRONMENT=development
   ```

4. **Start the database**
   ```bash
   docker compose up -d postgres
   ```

5. **Run migrations**
   ```bash
   task migrations-run
   # OR
   alembic upgrade head
   ```

6. **Seed the database (optional)**
   ```bash
   task database-seed
   # OR
   poetry run python seed_utility.py --seed
   ```

7. **Start the API**
   ```bash
   poetry run uvicorn main_api:app --reload
   ```

   API will be available at `http://localhost:8000`
   - Interactive docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## Development

### Using Docker Compose

Start the entire stack (database + API):
```bash
task env-dev-start
# OR
docker compose up --build
```

Stop the stack:
```bash
task env-dev-stop
# OR
docker compose down
```

### Code Quality

Format and lint your code:
```bash
task check
# OR
poetry run black .
poetry run isort .
poetry run ruff check . --fix
```

### Testing

Run the test suite:
```bash
task pytest
# OR
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest -v --cov=. --cov-report=html
```

### Database Operations

**Migrations:**
```bash
# Run all pending migrations
task migrations-run
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Downgrade one migration
task migrations-downgrade
alembic downgrade -1
```

**Seeding:**
```bash
# Seed with default data (10 auctions, 240 vehicles, 20 users)
task database-seed
poetry run python seed_utility.py --seed

# Custom seed amounts
poetry run python seed_utility.py --seed --auctions 20 --vehicles 500

# Clear all data
task database-clear
poetry run python seed_utility.py --clear

# Reset database (clear + seed)
task database-reset
poetry run python seed_utility.py --reset
```

## API Endpoints

### Auctions
- `GET /api/v1/auctions` - List all auctions
- `GET /api/v1/auctions/{id}` - Get auction by ID
- `POST /api/v1/auctions` - Create auction
- `PUT /api/v1/auctions/{id}` - Update auction
- `DELETE /api/v1/auctions/{id}` - Delete auction

### Vehicles
- `GET /api/v1/auction-vehicles` - List all auction vehicles
- `GET /api/v1/auction-vehicles/{id}` - Get vehicle by ID
- `POST /api/v1/auction-vehicles` - Create vehicle
- `PUT /api/v1/auction-vehicles/{id}` - Update vehicle
- `DELETE /api/v1/auction-vehicles/{id}` - Delete vehicle

### Manufacturers & Models
- `GET /api/v1/vehicle-manufacturers` - List all manufacturers
- `GET /api/v1/vehicle-models` - List all vehicle models

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user by ID

## Task Commands

The project uses [Task](https://taskfile.dev) for common operations:

```bash
# Environment
task env-dev-start        # Start development environment
task env-dev-stop         # Stop development environment
task env-test-start       # Start test database

# Code Quality
task check               # Format and lint code

# Testing
task pytest              # Run tests
task ci                  # Run full CI pipeline

# Database
task migrations-run      # Run migrations
task migrations-downgrade # Rollback one migration
task database-seed       # Seed database
task database-reset      # Reset database
task database-clear      # Clear all data
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_DB` | Database name | `auction_development` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_SCHEMA` | Database schema | `api` |
| `ENVIRONMENT` | Environment name | `development` |

## Architecture

The application follows a clean architecture pattern:

1. **Controllers** - Handle HTTP requests/responses
2. **Services** - Contain business logic
3. **Repositories** - Handle data access
4. **Models** - Define database schema
5. **Contracts** - Define API contracts with Pydantic

### Dependency Injection

The app uses `dependency-injector` for managing dependencies. Configuration is in `core/dependency_injection.py`.

### Database

- PostgreSQL 15 with async SQLAlchemy
- Schema-based multi-tenancy support
- Alembic for migrations
- Connection pooling and session management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Python 3.13+ type hints
- Line length: 120 characters
- Follow PEP 8 with Black formatting
- Imports sorted with isort (black profile)
- Docstrings for public APIs

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions, please open an issue in the GitHub repository.
