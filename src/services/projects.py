from typing import Sequence

import httpx
from httpx import AsyncClient
from sqlalchemy import select, func, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.logger import logger
from src.models.projects import Project
from src.schemas.projects import ProjectSchema


async def get_projects(session: AsyncSession, query: Select) -> Sequence[Project]:
    projects = await session.execute(query)
    return projects.scalars().all()


class ProjectService:
    @staticmethod
    async def find_projects(query: str) -> list[ProjectSchema] | None:
        try:
            async with AsyncClient() as client:
                logger.debug(f"Searching projects for {query}")
                response = await client.get(
                    "https://gitlab.com/api/v4/projects/",
                    params={"search": query},
                )
                data = response.json()

                return [
                    ProjectSchema(
                        id=project["id"],
                        name=project["name"],
                        description=project["description"],
                        last_activity=project["last_activity_at"],
                    )
                    for project in data
                ]
        except httpx.RequestError:
            logger.error("Error on request happen", exc_info=True)

    @staticmethod
    async def save_projects(
        session: AsyncSession,
        projects: list[ProjectSchema],
        query: str,
    ) -> Sequence[Project]:
        projects_data = [Project(**data.model_dump()) for data in projects]
        ilike_search = f"%{query}%"

        # TODO: Try to optimize queries
        count_projects_query = (
            select(
                func.count(),
            )
            .select_from(Project)
            .where(Project.name.ilike(ilike_search))
        )
        get_projects_query = select(Project).where(Project.name.ilike(ilike_search))

        try:
            result = await session.execute(count_projects_query)
            projects_quantity = result.scalar()

            if projects_quantity > 0:
                logger.debug("Return existing projects")
                return await get_projects(session, get_projects_query)

            session.add_all(projects_data)
            await session.commit()

            return await get_projects(session, get_projects_query)

        except SQLAlchemyError:
            logger.error("Error getting projects from DB", exc_info=True)
