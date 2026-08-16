from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.domain.entities.user import User
from app.domain.exceptions.user import EmailAlreadyExistsError
from app.infrastructure.databases.postgres.repositories.base_repo import (
    BaseRepository,
)


class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
        return self.db.scalar(statement)

    def create(self, entity: User) -> User:
        try:
            return super().create(entity)
        except IntegrityError as exc:
            raise EmailAlreadyExistsError(
                "Email already exists"
            ) from exc