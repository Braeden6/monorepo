from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.generate_status import GenerateStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_read import RecipeRead


T = TypeVar("T", bound="GenerateStatusResponse")


@_attrs_define
class GenerateStatusResponse:
    """
    Attributes:
        workflow_id (str):
        status (GenerateStatus):
        current_step (str): Current step: queued, generating, reviewing, fixing, saving, completed, failed
        recipes (list[RecipeRead] | None | Unset): Generated recipes (only present when completed)
        error (None | str | Unset): Error message (only present when failed)
    """

    workflow_id: str
    status: GenerateStatus
    current_step: str
    recipes: list[RecipeRead] | None | Unset = UNSET
    error: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        status = self.status.value

        current_step = self.current_step

        recipes: list[dict[str, Any]] | None | Unset
        if isinstance(self.recipes, Unset):
            recipes = UNSET
        elif isinstance(self.recipes, list):
            recipes = []
            for recipes_type_0_item_data in self.recipes:
                recipes_type_0_item = recipes_type_0_item_data.to_dict()
                recipes.append(recipes_type_0_item)

        else:
            recipes = self.recipes

        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        else:
            error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflow_id": workflow_id,
                "status": status,
                "current_step": current_step,
            }
        )
        if recipes is not UNSET:
            field_dict["recipes"] = recipes
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_read import RecipeRead

        d = dict(src_dict)
        workflow_id = d.pop("workflow_id")

        status = GenerateStatus(d.pop("status"))

        current_step = d.pop("current_step")

        def _parse_recipes(data: object) -> list[RecipeRead] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                recipes_type_0 = []
                _recipes_type_0 = data
                for recipes_type_0_item_data in _recipes_type_0:
                    recipes_type_0_item = RecipeRead.from_dict(recipes_type_0_item_data)

                    recipes_type_0.append(recipes_type_0_item)

                return recipes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[RecipeRead] | None | Unset, data)

        recipes = _parse_recipes(d.pop("recipes", UNSET))

        def _parse_error(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        generate_status_response = cls(
            workflow_id=workflow_id,
            status=status,
            current_step=current_step,
            recipes=recipes,
            error=error,
        )

        generate_status_response.additional_properties = d
        return generate_status_response

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
