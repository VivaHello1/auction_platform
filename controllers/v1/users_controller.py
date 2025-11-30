from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from contracts import UserRegistrationResponse, UserRegistrationUpdateRequest
from core.dependency_injection import Container
from services import UsersService

router = APIRouter(prefix="/api/v1")


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, operation_id="get_user")
@inject
async def get_user(
    user_id: int,
    service: Annotated[UsersService, Depends(Provide[Container.users_service])],
) -> UserRegistrationResponse:
    user = await service.users_repository.get_by_id(user_id)
    return await service.get_user(user)


@router.put("/users/{user_id}", status_code=status.HTTP_200_OK, operation_id="update_user")
@inject
async def update_user(
    user_id: int,
    request: UserRegistrationUpdateRequest,
    service: Annotated[UsersService, Depends(Provide[Container.users_service])],
) -> UserRegistrationResponse:
    existing_user = await service.users_repository.get_by_id(user_id)
    return await service.update_user(existing_user, request)
