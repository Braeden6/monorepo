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


T = TypeVar("T", bound="RecipeUpdate")


@_attrs_define
class RecipeUpdate:
    """
    Attributes:
        name (None | str | Unset):
        description (None | str | Unset):
        ingredients (list[IngredientItem] | None | Unset):
        instructions (None | str | Unset):
        food_type (FoodType | None | Unset):
        status (None | RecipeStatus | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    ingredients: list[IngredientItem] | None | Unset = UNSET
    instructions: None | str | Unset = UNSET
    food_type: FoodType | None | Unset = UNSET
    status: None | RecipeStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        ingredients: list[dict[str, Any]] | None | Unset
        if isinstance(self.ingredients, Unset):
            ingredients = UNSET
        elif isinstance(self.ingredients, list):
            ingredients = []
            for ingredients_type_0_item_data in self.ingredients:
                ingredients_type_0_item = ingredients_type_0_item_data.to_dict()
                ingredients.append(ingredients_type_0_item)

        else:
            ingredients = self.ingredients

        instructions: None | str | Unset
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        food_type: None | str | Unset
        if isinstance(self.food_type, Unset):
            food_type = UNSET
        elif isinstance(self.food_type, FoodType):
            food_type = self.food_type.value
        else:
            food_type = self.food_type

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, RecipeStatus):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if food_type is not UNSET:
            field_dict["food_type"] = food_type
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_item import IngredientItem

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_ingredients(data: object) -> list[IngredientItem] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ingredients_type_0 = []
                _ingredients_type_0 = data
                for ingredients_type_0_item_data in _ingredients_type_0:
                    ingredients_type_0_item = IngredientItem.from_dict(ingredients_type_0_item_data)

                    ingredients_type_0.append(ingredients_type_0_item)

                return ingredients_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[IngredientItem] | None | Unset, data)

        ingredients = _parse_ingredients(d.pop("ingredients", UNSET))

        def _parse_instructions(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

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

        def _parse_status(data: object) -> None | RecipeStatus | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = RecipeStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RecipeStatus | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        recipe_update = cls(
            name=name,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            food_type=food_type,
            status=status,
        )

        recipe_update.additional_properties = d
        return recipe_update

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
