import json
import time
import uuid

from temporalio import activity

from recipe_api.features.generate.llm_service import GenerationLLMService
from recipe_api.features.generate.log_service import GenerationLogService
from recipe_api.features.generate.prompts import RecipePrompts
from recipe_api.features.generate.schemas import GenerateRecipeInput
from recipe_api.features.recipes.service import RecipeService
from recipe_api.shared.db import get_db_session
from recipe_api.shared.models.generation_log import LogGenerationStep as LogStep
from recipe_api.shared.models.recipe import GenerationStatus, GenerationStep
from recipe_api.shared.services.embeddings import EmbeddingService


@activity.defn
async def create_recipe_placeholder(input_data: dict) -> str:
    workflow_input = GenerateRecipeInput(**input_data)
    activity.logger.info(f"Creating placeholder for workflow: {workflow_input.workflow_id}")

    with get_db_session() as session:
        svc = RecipeService(session, EmbeddingService())
        recipe = svc.create_placeholder(
            user_id=workflow_input.user_id,
            workflow_id=workflow_input.workflow_id,
            prompt=workflow_input.prompt,
        )
        return str(recipe.id)


@activity.defn
async def generate_recipe_content(
    recipe_id: str,
    workflow_id: str,
    input_data: dict,
) -> dict:
    workflow_input = GenerateRecipeInput(**input_data)
    activity.logger.info(f"Generating recipe for: {workflow_input.prompt}")
    recipe_uuid = uuid.UUID(recipe_id)

    with get_db_session() as session:
        recipe_svc = RecipeService(session, EmbeddingService())
        recipe_svc.update_generation_status(
            recipe_uuid,
            step=GenerationStep.GENERATING,
            status=GenerationStatus.IN_PROGRESS,
        )

    llm_svc = GenerationLLMService()
    start_time = time.time()
    error = None
    parsed_data = None
    raw_response = ""

    try:
        parsed_data, raw_response, _ = llm_svc.generate_content(workflow_input)
        return parsed_data
    except Exception as e:
        error = str(e)
        raise
    finally:
        duration_ms = int((time.time() - start_time) * 1000)
        with get_db_session() as session:
            log_svc = GenerationLogService(session)
            log_svc.log_llm_call(
                recipe_id=recipe_uuid,
                workflow_id=workflow_id,
                step=LogStep.GENERATE,
                system_prompt=RecipePrompts.GENERATE_SYSTEM,
                user_prompt=RecipePrompts.build_generation_user_prompt(
                    workflow_input.prompt,
                    1,
                    workflow_input.ingredients,
                    workflow_input.dietary_restrictions,
                ),
                raw_response=raw_response,
                parsed_response=parsed_data,
                error=error,
                duration_ms=duration_ms,
            )


@activity.defn
async def review_recipe_quality(
    recipe_id: str,
    workflow_id: str,
    recipe_data: dict,
) -> dict:
    activity.logger.info(f"Reviewing recipe: {recipe_data.get('name', 'Unknown')}")
    recipe_uuid = uuid.UUID(recipe_id)

    with get_db_session() as session:
        recipe_svc = RecipeService(session, EmbeddingService())
        recipe_svc.update_generation_status(recipe_uuid, step=GenerationStep.REVIEWING)

    llm_svc = GenerationLLMService()
    start_time = time.time()
    error = None
    parsed_data = None
    raw_response = ""

    try:
        parsed_data, raw_response = llm_svc.review_quality(recipe_data)
        return parsed_data
    except Exception as e:
        error = str(e)
        raise
    finally:
        duration_ms = int((time.time() - start_time) * 1000)
        with get_db_session() as session:
            log_svc = GenerationLogService(session)
            log_svc.log_llm_call(
                recipe_id=recipe_uuid,
                workflow_id=workflow_id,
                step=LogStep.REVIEW,
                system_prompt=RecipePrompts.REVIEW_SYSTEM,
                user_prompt=RecipePrompts.build_review_user_prompt(
                    json.dumps([recipe_data], indent=2)
                ),
                raw_response=raw_response,
                parsed_response=parsed_data,
                error=error,
                duration_ms=duration_ms,
            )


@activity.defn
async def fix_recipe_issues(
    recipe_id: str,
    workflow_id: str,
    recipe_data: dict,
    review_data: dict,
) -> dict:
    if not review_data.get("needs_fixes", False):
        return recipe_data

    activity.logger.info(f"Fixing recipe: {recipe_data.get('name', 'Unknown')}")
    recipe_uuid = uuid.UUID(recipe_id)

    with get_db_session() as session:
        recipe_svc = RecipeService(session, EmbeddingService())
        recipe_svc.update_generation_status(recipe_uuid, step=GenerationStep.FIXING)

    llm_svc = GenerationLLMService()
    start_time = time.time()
    error = None
    parsed_data = None
    raw_response = ""

    try:
        parsed_data, raw_response = llm_svc.fix_issues(recipe_data, review_data)
        return parsed_data
    except Exception as e:
        error = str(e)
        # tech debt: should be better handling of error data
        return recipe_data
    finally:
        duration_ms = int((time.time() - start_time) * 1000)
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
            json.dumps(recipe_data, indent=2), json.dumps(issues, indent=2)
        )

        with get_db_session() as session:
            log_svc = GenerationLogService(session)
            log_svc.log_llm_call(
                recipe_id=recipe_uuid,
                workflow_id=workflow_id,
                step=LogStep.FIX,
                system_prompt=RecipePrompts.FIX_SYSTEM,
                user_prompt=prompt,
                raw_response=raw_response,
                parsed_response=parsed_data,
                error=error,
                duration_ms=duration_ms,
            )


@activity.defn
async def finalize_recipe(
    recipe_id: str,
    workflow_id: str,
    recipe_data: dict,
) -> str:
    activity.logger.info(f"Finalizing recipe: {recipe_data.get('name', 'Unknown')}")

    with get_db_session() as session:
        svc = RecipeService(session, EmbeddingService())
        recipe = svc.finalize_generated_recipe(
            recipe_id=uuid.UUID(recipe_id),
            name=recipe_data["name"],
            description=recipe_data["description"],
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            food_type_str=recipe_data.get("food_type"),
        )
        return str(recipe.id)


@activity.defn
async def mark_recipe_failed(
    recipe_id: str,
    error: str,
) -> None:
    activity.logger.error(f"Marking recipe {recipe_id} as failed: {error}")
    with get_db_session() as session:
        svc = RecipeService(session, EmbeddingService())
        svc.update_generation_status(
            uuid.UUID(recipe_id), status=GenerationStatus.FAILED, error=error
        )
