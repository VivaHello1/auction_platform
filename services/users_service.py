import uuid

from sqlalchemy import func

from contracts import UserRegistrationResponse, UserRegistrationUpdateRequest
from mappers import UserMapper
from repositories import UsersRepository
from repositories.models import User as UserModel


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def get_user(self, user: UserModel) -> UserRegistrationResponse:
        return UserRegistrationResponse(user=UserMapper.to_contract(user))

    async def update_user(
        self, existing_user: UserModel, request: UserRegistrationUpdateRequest
    ) -> UserRegistrationResponse:
        if request.supervisor_id is not None:
            existing_user.supervisor_id = request.supervisor_id
        if request.phone_number is not None:
            existing_user.phone_number = request.phone_number
        if request.passport_number is not None:
            existing_user.passport_number = request.passport_number
        if request.address is not None:
            existing_user.address = request.address
        if request.language is not None:
            existing_user.language = request.language
        if request.email is not None:
            existing_user.email = request.email
        if request.status is not None:
            existing_user.status = request.status

        updated_user = await self.users_repository.update(existing_user)

        return UserRegistrationResponse(user=UserMapper.to_contract(updated_user))

    async def get_or_create(self, user_id: uuid.UUID | None) -> UserModel:
        user = await self.users_repository.get_by_id(user_id)
        if user:
            return user

        new_user = UserModel(status="new", registration_date=func.now())
        return await self.users_repository.create(new_user)
