from core.config import settings


class AppError(Exception):
    def __init__(
        self,
        message: str,
        payload: dict = None,
    ):
        self.message = message
        self.payload = payload or {}

    def to_dict(self):
        if settings.is_prod:
            return {"error": self.message}

        return {"error": self.message, "data": self.payload}
