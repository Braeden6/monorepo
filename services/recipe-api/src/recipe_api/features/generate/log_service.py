import uuid
from typing import Any

from sqlmodel import Session

from recipe_api.shared.config import settings
from recipe_api.shared.models.generation_log import GenerationLog
from recipe_api.shared.models.generation_log import LogGenerationStep as LogStep


class GenerationLogService:
    def __init__(self, session: Session):
        self.session = session

    def log_llm_call(
        self,
        recipe_id: uuid.UUID,
        workflow_id: str,
        step: LogStep,
        system_prompt: str,
        user_prompt: str,
        raw_response: str,
        parsed_response: Any | None,
        error: str | None,
        duration_ms: int,
    ) -> None:
        log = GenerationLog(
            recipe_id=recipe_id,
            workflow_id=workflow_id,
            step=step,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            raw_response=raw_response,
            parsed_response=parsed_response,
            success=error is None,
            error=error,
            model=settings.vllm_model,
            duration_ms=duration_ms,
        )
        self.session.add(log)
        self.session.commit()
