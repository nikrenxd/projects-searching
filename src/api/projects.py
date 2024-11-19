from fastapi import APIRouter, Request

from pydantic import TypeAdapter

from src.api.dependencies import SessionDep, RedisDep
from src.core.limiter import limiter
from src.schemas.projects import ProjectSchema
from src.services.projects import ProjectService

project_router = APIRouter(prefix="/search", tags=["project"])


@project_router.get("/", response_model=list[ProjectSchema])
@limiter.limit("2/second")
async def search_projects(
    request: Request,
    project_name: str,
    session: SessionDep,
    r: RedisDep,
):
    cached_result = await r.get("projects")
    type_adapter = TypeAdapter(list[ProjectSchema])

    if not cached_result:
        fetched_data = await ProjectService.find_projects(query=project_name)

        results = await ProjectService.save_projects(
            session=session,
            projects=fetched_data,
            query=project_name,
        )

        encoded_data = type_adapter.dump_json(fetched_data).decode("utf-8")

        await r.set("projects", encoded_data, 15)

        return results

    return type_adapter.validate_json(cached_result)
