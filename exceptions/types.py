from .base import AppError


class NotFoundError(AppError):
    def __init__(self, id: str | int, obj_class: str):
        super().__init__(
            message=f"{id} not found.",
            payload={"details": f"{obj_class} with id {id} not found."},
        )


class UnauthorizedError(AppError):
    def __init__(self):
        super().__init__(
            message="You are not authorized to perform this action.",
        )
