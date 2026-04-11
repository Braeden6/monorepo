from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pagination_meta import PaginationMeta
    from ..models.recipe_query_response_filters_applied import RecipeQueryResponseFiltersApplied
    from ..models.recipe_read import RecipeRead


T = TypeVar("T", bound="RecipeQueryResponse")


@_attrs_define
class RecipeQueryResponse:
    """Response for recipe queries with pagination metadata.

    Attributes:
        results (list[RecipeRead]):
        pagination (PaginationMeta): Pagination metadata for cursor-based pagination.
        query (None | str | Unset): The search query if provided
        filters_applied (RecipeQueryResponseFiltersApplied | Unset): Summary of filters that were applied
    """

    results: list[RecipeRead]
    pagination: PaginationMeta
    query: None | str | Unset = UNSET
    filters_applied: RecipeQueryResponseFiltersApplied | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        pagination = self.pagination.to_dict()

        query: None | str | Unset
        if isinstance(self.query, Unset):
            query = UNSET
        else:
            query = self.query

        filters_applied: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters_applied, Unset):
            filters_applied = self.filters_applied.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "results": results,
                "pagination": pagination,
            }
        )
        if query is not UNSET:
            field_dict["query"] = query
        if filters_applied is not UNSET:
            field_dict["filters_applied"] = filters_applied

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pagination_meta import PaginationMeta
        from ..models.recipe_query_response_filters_applied import RecipeQueryResponseFiltersApplied
        from ..models.recipe_read import RecipeRead

        d = dict(src_dict)
        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = RecipeRead.from_dict(results_item_data)

            results.append(results_item)

        pagination = PaginationMeta.from_dict(d.pop("pagination"))

        def _parse_query(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        query = _parse_query(d.pop("query", UNSET))

        _filters_applied = d.pop("filters_applied", UNSET)
        filters_applied: RecipeQueryResponseFiltersApplied | Unset
        if isinstance(_filters_applied, Unset):
            filters_applied = UNSET
        else:
            filters_applied = RecipeQueryResponseFiltersApplied.from_dict(_filters_applied)

        recipe_query_response = cls(
            results=results,
            pagination=pagination,
            query=query,
            filters_applied=filters_applied,
        )

        recipe_query_response.additional_properties = d
        return recipe_query_response

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
