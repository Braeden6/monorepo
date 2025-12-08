from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateRequest")


@_attrs_define
class GenerateRequest:
    """
    Attributes:
        prompt (str): Description of what kind of recipe to generate
        amount (int | Unset): Number of recipes to generate Default: 1.
        ingredients (list[str] | None | Unset): Ingredients to include in the recipe
        dietary_restrictions (list[str] | None | Unset): Dietary restrictions to follow
    """

    prompt: str
    amount: int | Unset = 1
    ingredients: list[str] | None | Unset = UNSET
    dietary_restrictions: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        amount = self.amount

        ingredients: list[str] | None | Unset
        if isinstance(self.ingredients, Unset):
            ingredients = UNSET
        elif isinstance(self.ingredients, list):
            ingredients = self.ingredients

        else:
            ingredients = self.ingredients

        dietary_restrictions: list[str] | None | Unset
        if isinstance(self.dietary_restrictions, Unset):
            dietary_restrictions = UNSET
        elif isinstance(self.dietary_restrictions, list):
            dietary_restrictions = self.dietary_restrictions

        else:
            dietary_restrictions = self.dietary_restrictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if dietary_restrictions is not UNSET:
            field_dict["dietary_restrictions"] = dietary_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prompt = d.pop("prompt")

        amount = d.pop("amount", UNSET)

        def _parse_ingredients(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ingredients_type_0 = cast(list[str], data)

                return ingredients_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        ingredients = _parse_ingredients(d.pop("ingredients", UNSET))

        def _parse_dietary_restrictions(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                dietary_restrictions_type_0 = cast(list[str], data)

                return dietary_restrictions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        dietary_restrictions = _parse_dietary_restrictions(d.pop("dietary_restrictions", UNSET))

        generate_request = cls(
            prompt=prompt,
            amount=amount,
            ingredients=ingredients,
            dietary_restrictions=dietary_restrictions,
        )

        generate_request.additional_properties = d
        return generate_request

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
