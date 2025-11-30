from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.config import settings
from core.logging import logger
from exceptions.base import AppError
from exceptions.types import NotFoundError


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except NotFoundError as nfe:
            logger.error(f"NotFoundException: {nfe.message} - {nfe.payload}")
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nfe.to_dict())

        except AppError as ae:
            logger.error(f"AppException: {ae.message} - {ae.payload}")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=ae.to_dict())

        except Exception as e:
            logger.exception("Unhandled Exception")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_error",
                    "message": "An unexpected error occurred.",
                    "details": str(e) if settings.is_dev else None,
                },
            )
