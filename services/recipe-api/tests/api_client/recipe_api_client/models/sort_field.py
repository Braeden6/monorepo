from enum import Enum


class SortField(str, Enum):
    CREATED_AT = "created_at"
    FAVORITE_COUNT = "favorite_count"
    LIKE_COUNT = "like_count"
    RELEVANCE = "relevance"
    UPDATED_AT = "updated_at"

    def __str__(self) -> str:
        return str(self.value)
