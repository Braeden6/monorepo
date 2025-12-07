
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql://recipe:recipe@localhost:5432/recipe_db"

    # Clerk Authentication
    clerk_secret_key: str
    clerk_publishable_key: str

    # vLLM Service
    vllm_base_url: str = "http://localhost:8000"
    vllm_model: str = "Qwen/Qwen2.5-1.5B-Instruct-AWQ"
    vllm_api_key: str | None = None

    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    api_reload: bool = True
    log_level: str = "info"

    # CORS
    cors_origins: str | list[str] = "http://localhost:3000,http://localhost:3001"

    # Temporal
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "recipe-generation"
    worker_max_concurrent_activities: int = 100
    worker_max_concurrent_workflow_tasks: int = 100
    llm_retry_initial_interval_seconds: float = 1.0
    llm_retry_backoff_coefficient: float = 2.0
    llm_retry_max_attempts: int = 3
    llm_retry_max_interval_seconds: int = 30

    @property
    def cors_origins_list(self) -> list[str]:
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

settings = Settings()  # type: ignore[call-arg]
