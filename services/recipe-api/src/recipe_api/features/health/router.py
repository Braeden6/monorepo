
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Recipe API", "version": "0.1.0"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
