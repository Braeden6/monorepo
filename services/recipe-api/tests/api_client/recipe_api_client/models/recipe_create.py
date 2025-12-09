from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.food_type import FoodType
from ..models.recipe_status import RecipeStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_item import IngredientItem


T = TypeVar("T", bound="RecipeCreate")


@_attrs_define
class RecipeCreate:
    """
    Attributes:
        name (str):
        description (str):
        ingredients (list[IngredientItem]):
        instructions (str):
        food_type (FoodType | None | Unset):
        status (RecipeStatus | Unset):
    """

    name: str
    description: str
    ingredients: list[IngredientItem]
    instructions: str
    food_type: FoodType | None | Unset = UNSET
    status: RecipeStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        instructions = self.instructions

        food_type: None | str | Unset
        if isinstance(self.food_type, Unset):
            food_type = UNSET
        elif isinstance(self.food_type, FoodType):
            food_type = self.food_type.value
        else:
            food_type = self.food_type

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
            }
        )
        if food_type is not UNSET:
            field_dict["food_type"] = food_type
        if status is not UNSET:
            field_dict["status"] = status

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

        _status = d.pop("status", UNSET)
        status: RecipeStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = RecipeStatus(_status)

        recipe_create = cls(
            name=name,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            food_type=food_type,
            status=status,
        )

        recipe_create.additional_properties = d
        return recipe_create

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
