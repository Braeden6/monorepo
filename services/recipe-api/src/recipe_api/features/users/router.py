import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from recipe_api.features.recipes.schemas import RecipeRead
from recipe_api.features.users.service import UserService
from recipe_api.shared.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


@router.post("/recipes/{recipe_id}/favorite", status_code=status.HTTP_200_OK)
def toggle_favorite(
    recipe_id: uuid.UUID,
    current_user: CurrentUserDep,
    service: Annotated[UserService, Depends(get_user_service)],
) -> dict[str, bool]:
    return service.toggle_favorite(recipe_id, current_user)


@router.post("/recipes/{recipe_id}/like", status_code=status.HTTP_200_OK)
def toggle_like(
    recipe_id: uuid.UUID,
    current_user: CurrentUserDep,
    service: Annotated[UserService, Depends(get_user_service)],
) -> dict[str, bool]:
    return service.toggle_like(recipe_id, current_user)


@router.get("/me/favorites")
def get_my_favorites(
    current_user: CurrentUserDep,
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[RecipeRead]:
    return service.get_my_favorites(current_user)
