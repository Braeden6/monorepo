from functools import lru_cache

from sentence_transformers import SentenceTransformer

from recipe_api.shared.config import settings


class EmbeddingService:

    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.embedding_model)
        self.dimension = settings.embedding_dimension

    def encode(self, text: str) -> list[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
