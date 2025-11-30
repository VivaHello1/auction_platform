from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from contracts import AuctionsListQuery, AuctionVehiclesQuery, PaginationParams
from controllers import (
    auction_vehicles_router,
    auctions_router,
    health_router,
    manufacturers_router,
    users_router,
)
from core import UVICORN_LOGGING_CONFIG, logger, settings
from core.dependency_injection import create_container
from middlewares import ExceptionMiddleware, RequestMiddleware, validation_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the application with Uvicorn, environment: %s", settings.ENVIRONMENT)

    yield

    await app.container.db().close_db()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="AutoBid API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS (Modify origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ExceptionMiddleware)
app.add_middleware(RequestMiddleware)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include API routers
app.include_router(health_router)
app.include_router(auctions_router)
app.include_router(auction_vehicles_router)
app.include_router(manufacturers_router)
app.include_router(users_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="AutoBid API service",
        routes=app.routes,
    )

    openapi_schema["components"]["schemas"]["PaginationParams"] = PaginationParams.model_json_schema()
    openapi_schema["components"]["schemas"]["AuctionsListQuery"] = AuctionsListQuery.model_json_schema()
    openapi_schema["components"]["schemas"]["AuctionVehiclesQuery"] = AuctionVehiclesQuery.model_json_schema()

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Custom OpenAPI schema for parameter model rendering
app.openapi = custom_openapi

# Dependency injection
app.container = create_container()


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Running AutoBid API", "version": settings.PROJECT_VERSION}


if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        reload=True,
        log_config=UVICORN_LOGGING_CONFIG,
    )
