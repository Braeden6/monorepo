from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.food_type import FoodType
from ..models.recipe_status import RecipeStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_item import IngredientItem


T = TypeVar("T", bound="RecipeSearchResult")


@_attrs_define
class RecipeSearchResult:
    """
    Attributes:
        name (str):
        description (str):
        ingredients (list[IngredientItem]):
        instructions (str):
        id (UUID):
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        like_count (int):
        favorite_count (int):
        status (RecipeStatus):
        is_generated (bool):
        similarity_score (float):
        food_type (FoodType | None | Unset):
        is_liked (bool | Unset):  Default: False.
        is_favorited (bool | Unset):  Default: False.
    """

    name: str
    description: str
    ingredients: list[IngredientItem]
    instructions: str
    id: UUID
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    like_count: int
    favorite_count: int
    status: RecipeStatus
    is_generated: bool
    similarity_score: float
    food_type: FoodType | None | Unset = UNSET
    is_liked: bool | Unset = False
    is_favorited: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        instructions = self.instructions

        id = str(self.id)

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        like_count = self.like_count

        favorite_count = self.favorite_count

        status = self.status.value

        is_generated = self.is_generated

        similarity_score = self.similarity_score

        food_type: None | str | Unset
        if isinstance(self.food_type, Unset):
            food_type = UNSET
        elif isinstance(self.food_type, FoodType):
            food_type = self.food_type.value
        else:
            food_type = self.food_type

        is_liked = self.is_liked

        is_favorited = self.is_favorited

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
                "id": id,
                "created_by": created_by,
                "created_at": created_at,
                "updated_at": updated_at,
                "like_count": like_count,
                "favorite_count": favorite_count,
                "status": status,
                "is_generated": is_generated,
                "similarity_score": similarity_score,
            }
        )
        if food_type is not UNSET:
            field_dict["food_type"] = food_type
        if is_liked is not UNSET:
            field_dict["is_liked"] = is_liked
        if is_favorited is not UNSET:
            field_dict["is_favorited"] = is_favorited

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_item import IngredientItem

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = IngredientItem.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        instructions = d.pop("instructions")

        id = UUID(d.pop("id"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        like_count = d.pop("like_count")

        favorite_count = d.pop("favorite_count")

        status = RecipeStatus(d.pop("status"))

        is_generated = d.pop("is_generated")

        similarity_score = d.pop("similarity_score")

        def _parse_food_type(data: object) -> FoodType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                food_type_type_0 = FoodType(data)

                return food_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FoodType | None | Unset, data)

        food_type = _parse_food_type(d.pop("food_type", UNSET))

        is_liked = d.pop("is_liked", UNSET)

        is_favorited = d.pop("is_favorited", UNSET)

        recipe_search_result = cls(
            name=name,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            id=id,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            like_count=like_count,
            favorite_count=favorite_count,
            status=status,
            is_generated=is_generated,
            similarity_score=similarity_score,
            food_type=food_type,
            is_liked=is_liked,
            is_favorited=is_favorited,
        )

        recipe_search_result.additional_properties = d
        return recipe_search_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
