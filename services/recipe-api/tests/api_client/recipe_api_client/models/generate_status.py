from enum import Enum


class GenerateStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    FIXING = "fixing"
    GENERATING = "generating"
    PENDING = "pending"
    REVIEWING = "reviewing"

    def __str__(self) -> str:
        return str(self.value)
