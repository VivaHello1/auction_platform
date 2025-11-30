import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.logging import logger


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        method = request.method
        url = request.url.path
        if request.url.query:
            url += f"?{request.url.query}"

        http_version = f"HTTP/{request.scope.get('http_version', '1.1')}"

        start_time = time.time()

        response = await call_next(request)

        duration_ms = int((time.time() - start_time) * 1000)

        status_code = response.status_code
        logger.info(f'{client_host}:{client_port} - "{method} {url} {http_version}" {status_code} {duration_ms}ms')

        return response
