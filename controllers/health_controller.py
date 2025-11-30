from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from core.dependency_injection import Container
from database.database import Database

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "healthy"}


@router.get("/ready")
@inject
async def readiness(db: Annotated[Database, Depends(Provide[Container.db])]):
    """Health check with database connectivity verification."""
    health_status = {"status": "ready", "checks": {"database": "unknown"}}

    try:
        # Test database connection
        async with db.session_factory() as session:
            # Simple query to test connection
            await session.execute(text("SELECT 1"))
            health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = "unhealthy"
        health_status["error"] = str(e)

        # Return 503 Service Unavailable for unhealthy status
        raise HTTPException(status_code=503, detail=health_status) from None

    return health_status
