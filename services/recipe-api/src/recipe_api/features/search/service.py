import json

from sqlmodel import Session, select

from recipe_api.features.recipes.schemas import RecipeCreate, RecipeRead
from recipe_api.features.search.schemas import RecipeSearchResult
from recipe_api.shared.models.recipe import FoodType, Recipe, RecipeStatus
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

    def generate_recipe(
        self,
        session: Session,
        prompt: str,
        user_id: str,
        amount: int = 1,
        ingredients: list[str] | None = None,
        dietary_restrictions: list[str] | None = None,
    ) -> list[RecipeRead]:
        system_prompt = """You are a professional chef and recipe creator. 
Generate creative, detailed, and practical recipes in JSON format.
Always include: name, description, ingredients (with amounts and units), instructions, and food_type.
Food types must be one of: breakfast, lunch, dinner, dessert, snack, drink.
Make sure the recipe is realistic and can actually be made."""

        user_prompt = f"Create {amount} recipe(s) for: {prompt}\n\n"

        if ingredients:
            user_prompt += f"Using these ingredients: {', '.join(ingredients)}\n"

        if dietary_restrictions:
            user_prompt += (
                f"Dietary restrictions: {', '.join(dietary_restrictions)}\n"
            )

        user_prompt += """
Return ONLY a JSON object with a "recipes" key containing a list of recipe objects.
Example structure:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "description": "Brief description",
      "ingredients": [
        {"name": "ingredient", "amount": "2", "unit": "cups"}
      ],
      "instructions": "Step 1: ...",
      "food_type": "dinner"
    }
  ]
}
"""

        response = self.llm_service.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.8,
        )

        generated_recipes = []
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            data = json.loads(response)
            recipes_data = data.get("recipes", [])

            if isinstance(recipes_data, dict):
                recipes_data = [recipes_data]
            elif isinstance(data, list):
                recipes_data = data

            for recipe_data in recipes_data:
                if isinstance(recipe_data.get("instructions"), list):
                    recipe_data["instructions"] = "\n".join(recipe_data["instructions"])

                if recipe_data.get("food_type") not in [t.value for t in FoodType]:
                    recipe_data["food_type"] = None

                recipe_create = RecipeCreate(
                    **recipe_data,
                )

                recipe_dict = recipe_create.model_dump()
                recipe_dict["ingredients"] = [i.model_dump() for i in recipe_create.ingredients]
                recipe_dict["created_by"] = user_id
                recipe_dict["status"] = RecipeStatus.DRAFT
                recipe_dict["is_generated"] = True

                db_recipe = Recipe.model_validate(recipe_dict)

                # tech debt: embeddings are not generated her

                session.add(db_recipe)
                generated_recipes.append(db_recipe)

            session.commit()
            for r in generated_recipes:
                session.refresh(r)

            return [RecipeRead.model_validate(r) for r in generated_recipes]

        except (json.JSONDecodeError, KeyError) as e:
            # tech debt: error handling
            print(f"Error parsing generated recipes: {e}")
            return []
