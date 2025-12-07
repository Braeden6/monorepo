from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from temporalio.client import Client

from recipe_api.features.generate.schemas import (
    GenerateRequest,
    GenerateResponse,
    GenerateStatus,
    GenerateStatusResponse,
)
from recipe_api.features.generate.service import GenerateService
from recipe_api.shared.deps import CurrentUserDep, SessionDep
from recipe_api.shared.rate_limit import get_rate_limit_key
from recipe_api.shared.temporal import get_temporal_client

router = APIRouter(prefix="/generate", tags=["generate"])


async def get_generate_service(
    session: SessionDep,
    temporal_client: Annotated[Client, Depends(get_temporal_client)],
) -> GenerateService:
    return GenerateService(temporal_client, session)


@router.post(
    "/",
    response_model=GenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Start recipe generation",
    dependencies=[Depends(RateLimiter(times=5, hours=1, identifier=get_rate_limit_key))],
)
async def start_generation(
    request: GenerateRequest,
    current_user: CurrentUserDep,
    service: Annotated[GenerateService, Depends(get_generate_service)],
) -> GenerateResponse:
    try:
        base_workflow_id, _ = await service.start_generation(request, current_user)
        return GenerateResponse(
            workflow_id=base_workflow_id,
            status=GenerateStatus.PENDING,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to start generation workflow: {e!s}",
        ) from e


@router.get(
    "/{workflow_id}",
    response_model=GenerateStatusResponse,
    summary="Get generation status",
)
async def get_generation_status(
    workflow_id: str,
    current_user: CurrentUserDep,
    service: Annotated[GenerateService, Depends(get_generate_service)],
) -> GenerateStatusResponse:
    result = await service.get_status(workflow_id)

    return GenerateStatusResponse(
        workflow_id=result["workflow_id"],
        status=result["status"],
        current_step=result["current_step"],
        recipes=result["recipes"],
        error=result["error"],
    )
