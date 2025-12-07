from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import asyncio as aioredis

from recipe_api.features.generate.router import router as generate_router
from recipe_api.features.health.router import router as health_router
from recipe_api.features.recipes.router import router as recipes_router
from recipe_api.features.search.router import router as search_router
from recipe_api.features.users.router import router as users_router
from recipe_api.shared.config import settings
from recipe_api.shared.rate_limit import get_rate_limit_key


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield
    await redis.close()

app = FastAPI(
    title="Recipe API",
    description="Recipe management API with RAG search and LLM generation",
    version="0.1.0",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
    dependencies=[Depends(RateLimiter(times=60, seconds=60, identifier=get_rate_limit_key))],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes_router)
app.include_router(search_router)
app.include_router(users_router)
app.include_router(generate_router)
app.include_router(health_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host=settings.api_host, port=settings.api_port, reload=True)
