from app.domain.entities.user import User
from app.domain.exceptions.user import EmailAlreadyExistsError
from app.infrastructure.databases.postgres.repositories.user import (
    UserRepository,
)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all(self) -> list[User]:
        return self.user_repository.get_all()

    def get_by_id(self, user_id: int) -> User | None:
        return self.user_repository.get_by_id(user_id)

    def create(self, user: User) -> User:
        existing_user = self.user_repository.get_by_email(user.email)

        if existing_user is not None:
            raise EmailAlreadyExistsError(
                "Email already exists"
            )

        return self.user_repository.create(user)

    def update(self, user: User) -> User:
        existing_user = self.user_repository.get_by_email(user.email)

        if (
            existing_user is not None
            and existing_user.id != user.id
        ):
            raise EmailAlreadyExistsError(
                "Email already exists"
            )

        return self.user_repository.update(user)

    def delete(
        self,
        user: User,
        hard_delete: bool = False,
    ) -> None:
        self.user_repository.delete(
            user,
            hard_delete=hard_delete,
        )