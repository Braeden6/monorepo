import json
import time

import instructor
from openai import OpenAI

from recipe_api.features.generate.prompts import RecipePrompts
from recipe_api.features.generate.schemas import (
    FixedRecipe,
    GeneratedRecipe,
    GenerateRecipeInput,
    RecipeReviewList,
)
from recipe_api.shared.config import settings

_cached_client: instructor.Instructor | None = None


class GenerationLLMService:
    def __init__(self) -> None:
        pass

    @property
    def client(self) -> instructor.Instructor:
        return self._get_instructor_client()

    def _get_instructor_client(self) -> instructor.Instructor:
        global _cached_client
        if _cached_client is None:
            openai_client = OpenAI(
                base_url=settings.vllm_base_url,
                api_key=settings.vllm_api_key or "EMPTY",
            )
            _cached_client = instructor.from_openai(
                openai_client, mode=instructor.Mode.JSON
            )
        return _cached_client

    def generate_content(
        self,
        input_data: GenerateRecipeInput,
    ) -> tuple[dict, str, int]:

        prompt = RecipePrompts.build_generation_user_prompt(
            prompt=input_data.prompt,
            amount=1,
            ingredients=input_data.ingredients,
            dietary_restrictions=input_data.dietary_restrictions,
        )

        start_time = time.time()
        try:
            result = self.client.chat.completions.create(
                model=settings.vllm_model,
                messages=[
                    {"role": "system", "content": RecipePrompts.GENERATE_SYSTEM},
                    {"role": "user", "content": prompt},
                ],
                response_model=GeneratedRecipe,
                max_tokens=1024,
                temperature=0.7,
                max_retries=2,
            )
            data = result.model_dump()
            return data, json.dumps(data), int((time.time() - start_time) * 1000)
        except Exception:
            raise

    def review_quality(self, recipe_data: dict) -> tuple[dict, str]:
        recipes_json = json.dumps([recipe_data], indent=2)
        prompt = RecipePrompts.build_review_user_prompt(recipes_json)

        result = self.client.chat.completions.create(
            model=settings.vllm_model,
            messages=[
                {"role": "system", "content": RecipePrompts.REVIEW_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            response_model=RecipeReviewList,
            max_tokens=1024,
            temperature=0.3,
            max_retries=2,
        )

        if result.reviews:
            data = result.reviews[0].model_dump()
            return data, json.dumps(data)

        return {"needs_fixes": False}, "{}"

    def fix_issues(
        self,
        recipe_data: dict,
        review_data: dict,
    ) -> tuple[dict, str]:
        issues = {
            k: v
            for k, v in review_data.items()
            if k
            in [
                "food_type_valid",
                "food_type_suggestion",
                "ingredient_issues",
                "realism_issues",
                "instruction_issues",
            ]
            and v
        }

        prompt = RecipePrompts.build_fix_user_prompt(
            recipe_json=json.dumps(recipe_data, indent=2),
            issues_json=json.dumps(issues, indent=2),
        )

        result = self.client.chat.completions.create(
            model=settings.vllm_model,
            messages=[
                {"role": "system", "content": RecipePrompts.FIX_SYSTEM},
                {"role": "user", "content": prompt},
            ],
            response_model=FixedRecipe,
            max_tokens=1024,
            temperature=0.5,
            max_retries=2,
        )

        parsed_data = {
            "name": result.name,
            "description": result.description,
            "ingredients": [ing.model_dump() for ing in result.ingredients],
            "instructions": result.instructions,
            "food_type": result.food_type.value,
        }
        return parsed_data, json.dumps(result.model_dump())
