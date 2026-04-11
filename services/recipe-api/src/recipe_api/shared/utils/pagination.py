import base64
import json
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass
class CursorData:
    offset: int
    sort_field: str
    sort_value: Any | None = None
    item_id: str | None = None


def encode_cursor(offset: int, sort_field: str, item_id: str | None) -> str | None:
    if item_id is None:
        return None
    data = {"o": offset, "f": sort_field, "id": item_id}
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()


def decode_cursor(cursor: str) -> CursorData:
    try:
        data = json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
        return CursorData(
            offset=data.get("o", 0),
            sort_field=data.get("f", "created_at"),
            sort_value=data.get("v"),
            item_id=data.get("id"),
        )
    except (ValueError, KeyError, json.JSONDecodeError):
        return CursorData(offset=0, sort_field="created_at", sort_value=None, item_id=None)
