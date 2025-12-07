from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recipe_api.features.generate.router import router as generate_router
from recipe_api.features.recipes.router import router as recipes_router
from recipe_api.features.search.router import router as search_router
from recipe_api.features.users.router import router as users_router
from recipe_api.shared.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield

app = FastAPI(
    title="Recipe API",
    description="Recipe management API with RAG search and LLM generation",
    version="0.1.0",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
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

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Recipe API", "version": "0.1.0"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host=settings.api_host, port=settings.api_port, reload=True)
