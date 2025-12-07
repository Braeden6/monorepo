
from sqlmodel import Session, select

from recipe_api.features.search.schemas import RecipeSearchResult
from recipe_api.shared.models.recipe import Recipe, RecipeStatus
from recipe_api.shared.models.user_interaction import UserRecipeInteraction
from recipe_api.shared.services.embeddings import EmbeddingService
from recipe_api.shared.services.llm import LLMService


class SearchService:
    def __init__(self, embedding_service: EmbeddingService, llm_service: LLMService):
        self.embedding_service = embedding_service
        self.llm_service = llm_service

    def search_recipes(
        self,
        session: Session,
        query: str,
        limit: int = 10,
        user_id: str | None = None,
    ) -> list[RecipeSearchResult]:

        from sqlalchemy import func

        query_embedding = self.embedding_service.encode(query)

        desc_similarity = 1 - Recipe.description_embedding.cosine_distance(query_embedding)
        ing_similarity = 1 - Recipe.ingredient_embedding.cosine_distance(query_embedding)
        max_similarity = func.greatest(desc_similarity, ing_similarity)

        stmt = (
            select(
                Recipe,
                desc_similarity.label("desc_similarity"),
                ing_similarity.label("ing_similarity"),
                max_similarity.label("max_similarity"),
            )
            .where(
                Recipe.description_embedding.is_not(None),
                Recipe.ingredient_embedding.is_not(None),
                Recipe.status == RecipeStatus.PUBLISHED,
            )
            .order_by(max_similarity.desc())
            .limit(limit)
        )

        result = session.exec(stmt)

        recipes = []
        for row in result:
            recipe = row[0]
            max_sim = row[3]

            is_liked = False
            is_favorited = False
            if user_id:
                interaction = session.exec(
                    select(UserRecipeInteraction).where(
                        UserRecipeInteraction.user_id == user_id,
                        UserRecipeInteraction.recipe_id == recipe.id,
                    )
                ).first()
                if interaction:
                    is_liked = interaction.is_liked
                    is_favorited = interaction.is_favorite

            recipes.append(
                RecipeSearchResult(
                    **recipe.model_dump(),
                    similarity_score=max_sim,
                    is_liked=is_liked,
                    is_favorited=is_favorited,
                )
            )

        return recipes

    def hybrid_search(
        self,
        session: Session,
        query: str,
        limit: int = 10,
        user_id: str | None = None,
        boost_popular: bool = True,
    ) -> list[RecipeSearchResult]:
        results = self.search_recipes(session, query, limit * 2, user_id)

        if boost_popular:
            for result in results:
                popularity_score = (result.like_count + result.favorite_count * 2) / 100
                result.similarity_score = (
                    result.similarity_score * 0.7 + popularity_score * 0.3
                )

            results.sort(key=lambda x: x.similarity_score, reverse=True)

        return results[:limit]
