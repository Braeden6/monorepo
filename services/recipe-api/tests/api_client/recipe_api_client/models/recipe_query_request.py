from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.food_type import FoodType
from ..models.sort_field import SortField
from ..models.sort_order import SortOrder
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeQueryRequest")


@_attrs_define
class RecipeQueryRequest:
    """Unified query request for searching and filtering recipes.

    Attributes:
        query (None | str | Unset): Text query for semantic search (RAG).
        food_types (list[FoodType] | None | Unset): Filter by one or more food types
        include_drafts (bool | Unset): Include your own draft recipes (only applies when authenticated) Default: True.
        only_mine (bool | Unset): Only return recipes created by you Default: False.
        only_favorites (bool | Unset): Only return recipes you have favorited Default: False.
        sort_by (SortField | Unset): Available fields for sorting recipes.
        sort_order (SortOrder | Unset): Sort direction.
        limit (int | Unset): Maximum number of results to return Default: 20.
        cursor (None | str | Unset): Pagination cursor from previous response
        boost_popular (bool | Unset): Boost popular recipes in search results Default: True.
    """

    query: None | str | Unset = UNSET
    food_types: list[FoodType] | None | Unset = UNSET
    include_drafts: bool | Unset = True
    only_mine: bool | Unset = False
    only_favorites: bool | Unset = False
    sort_by: SortField | Unset = UNSET
    sort_order: SortOrder | Unset = UNSET
    limit: int | Unset = 20
    cursor: None | str | Unset = UNSET
    boost_popular: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query: None | str | Unset
        if isinstance(self.query, Unset):
            query = UNSET
        else:
            query = self.query

        food_types: list[str] | None | Unset
        if isinstance(self.food_types, Unset):
            food_types = UNSET
        elif isinstance(self.food_types, list):
            food_types = []
            for food_types_type_0_item_data in self.food_types:
                food_types_type_0_item = food_types_type_0_item_data.value
                food_types.append(food_types_type_0_item)

        else:
            food_types = self.food_types

        include_drafts = self.include_drafts

        only_mine = self.only_mine

        only_favorites = self.only_favorites

        sort_by: str | Unset = UNSET
        if not isinstance(self.sort_by, Unset):
            sort_by = self.sort_by.value

        sort_order: str | Unset = UNSET
        if not isinstance(self.sort_order, Unset):
            sort_order = self.sort_order.value

        limit = self.limit

        cursor: None | str | Unset
        if isinstance(self.cursor, Unset):
            cursor = UNSET
        else:
            cursor = self.cursor

        boost_popular = self.boost_popular

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if query is not UNSET:
            field_dict["query"] = query
        if food_types is not UNSET:
            field_dict["food_types"] = food_types
        if include_drafts is not UNSET:
            field_dict["include_drafts"] = include_drafts
        if only_mine is not UNSET:
            field_dict["only_mine"] = only_mine
        if only_favorites is not UNSET:
            field_dict["only_favorites"] = only_favorites
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if sort_order is not UNSET:
            field_dict["sort_order"] = sort_order
        if limit is not UNSET:
            field_dict["limit"] = limit
        if cursor is not UNSET:
            field_dict["cursor"] = cursor
        if boost_popular is not UNSET:
            field_dict["boost_popular"] = boost_popular

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_query(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        query = _parse_query(d.pop("query", UNSET))

        def _parse_food_types(data: object) -> list[FoodType] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                food_types_type_0 = []
                _food_types_type_0 = data
                for food_types_type_0_item_data in _food_types_type_0:
                    food_types_type_0_item = FoodType(food_types_type_0_item_data)

                    food_types_type_0.append(food_types_type_0_item)

                return food_types_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FoodType] | None | Unset, data)

        food_types = _parse_food_types(d.pop("food_types", UNSET))

        include_drafts = d.pop("include_drafts", UNSET)

        only_mine = d.pop("only_mine", UNSET)

        only_favorites = d.pop("only_favorites", UNSET)

        _sort_by = d.pop("sort_by", UNSET)
        sort_by: SortField | Unset
        if isinstance(_sort_by, Unset):
            sort_by = UNSET
        else:
            sort_by = SortField(_sort_by)

        _sort_order = d.pop("sort_order", UNSET)
        sort_order: SortOrder | Unset
        if isinstance(_sort_order, Unset):
            sort_order = UNSET
        else:
            sort_order = SortOrder(_sort_order)

        limit = d.pop("limit", UNSET)

        def _parse_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cursor = _parse_cursor(d.pop("cursor", UNSET))

        boost_popular = d.pop("boost_popular", UNSET)

        recipe_query_request = cls(
            query=query,
            food_types=food_types,
            include_drafts=include_drafts,
            only_mine=only_mine,
            only_favorites=only_favorites,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit,
            cursor=cursor,
            boost_popular=boost_popular,
        )

        recipe_query_request.additional_properties = d
        return recipe_query_request

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
