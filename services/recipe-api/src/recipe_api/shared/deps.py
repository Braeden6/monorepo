from typing import Annotated

from clerk_backend_api import Clerk
from clerk_backend_api.security import verify_token
from clerk_backend_api.security.types import VerifyTokenOptions
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from recipe_api.shared.config import settings
from recipe_api.shared.db import get_session

clerk_client = Clerk(bearer_auth=settings.clerk_secret_key)

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    token = credentials.credentials

    try:
        verified_token = verify_token(
            token, VerifyTokenOptions(secret_key=settings.clerk_secret_key)
        )
        user_id = verified_token.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session: no user_id found",
            )
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        ) from e


def get_optional_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(optional_security)],
) -> str | None:
    if credentials is None:
        return None

    token = credentials.credentials
    try:
        verified_token = verify_token(
            token, VerifyTokenOptions(secret_key=settings.clerk_secret_key)
        )
        return verified_token.get("sub")
    except Exception:
        return None


SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[str, Depends(get_current_user_id)]
OptionalUserDep = Annotated[str | None, Depends(get_optional_user_id)]
