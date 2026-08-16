from datetime import UTC, datetime
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.base_entity import BaseEntity

EntityType = TypeVar("EntityType", bound=BaseEntity)


class BaseRepository(Generic[EntityType]):
    def __init__(
        self,
        model: type[EntityType],
        db: Session,
    ):
        self.model = model
        self.db = db

    def get_all(self) -> list[EntityType]:
        statement = select(self.model).where(
            self.model.deleted_at.is_(None)
        )

        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        entity_id: int,
    ) -> EntityType | None:
        statement = select(self.model).where(
            self.model.id == entity_id,
            self.model.deleted_at.is_(None),
        )

        return self.db.scalar(statement)

    def create(
        self,
        entity: EntityType,
    ) -> EntityType:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(
        self,
        entity: EntityType,
    ) -> EntityType:
        entity.updated_at = datetime.now(UTC)

        self.db.add(entity)
        return entity

    def delete(
        self,
        entity: EntityType,
        hard_delete: bool = False,
    ) -> None:
        if hard_delete:
            self.db.delete(entity)
        else:
            entity.deleted_at = datetime.now(UTC)
            self.db.add(entity)
