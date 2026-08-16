from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.services.user_service import UserService
from app.domain.entities.user import User
from app.domain.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from app.infrastructure.databases.postgres.db import get_db
from app.infrastructure.databases.postgres.repositories.user import (
    UserRepository,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.get(
    "",
    response_model=list[UserResponseSchema],
)
def get_users(
    service: UserService = Depends(get_user_service),
):
    return service.get_all()


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.post(
    "",
    response_model=UserResponseSchema,
    status_code=201,
)
def create_user(
    request: UserCreateSchema,
    service: UserService = Depends(get_user_service),
):
    user = User(
        name=request.name,
        email=str(request.email),
    )

    return service.create(user)


@router.put(
    "/{user_id}",
    response_model=UserResponseSchema,
)
def update_user(
    user_id: int,
    request: UserUpdateSchema,
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if request.name is not None:
        user.name = request.name

    if request.email is not None:
        user.email = str(request.email)

    return service.update(user)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    hard_delete: bool = False,
    service: UserService = Depends(get_user_service),
):
    user = service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    service.delete(
        user,
        hard_delete=hard_delete,
    )

    return {
        "message": "User deleted successfully",
    }