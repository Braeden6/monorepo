from clerk_backend_api.security import verify_token
from clerk_backend_api.security.types import VerifyTokenOptions
from fastapi import Request

from recipe_api.shared.config import settings


async def get_rate_limit_key(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            verified_token = verify_token(
                token, VerifyTokenOptions(secret_key=settings.clerk_secret_key)
            )
            user_id = verified_token.get("sub")
            if user_id:
                return f"user:{user_id}"
        except Exception:
            # Token invalid or expired, fall back to IP
            pass

    ip = request.client.host if request.client else "127.0.0.1"
    return f"ip:{ip}"
