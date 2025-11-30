from contracts import User
from repositories.models import User as UserModel


class UserMapper:
    @staticmethod
    def to_contract(user: UserModel) -> User:
        return User(
            id=user.id,
            supervisor_id=user.supervisor_id,
            phone_number=user.phone_number,
            passport_number=user.passport_number,
            address=user.address,
            language=user.language,
            email=user.email,
            registration_date=user.registration_date,
            comments=user.comments,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
