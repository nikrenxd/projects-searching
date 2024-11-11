from typing import Annotated

from fastapi import APIRouter, status, Depends, Request

from src.core.db import get_session
from src.core.limiter import limiter
from src.services.projects import ProjectService

project_router = APIRouter(prefix="/search", tags=["project"])


@project_router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("2/minute")
async def search_projects(
    request: Request,
    project_name: str,
    session: Annotated[get_session, Depends()],
):
    results = await ProjectService.search_projects(query=project_name)

    projects = await ProjectService.save_projects(
        session,
        projects=results,
        query=project_name,
    )

    return projects
