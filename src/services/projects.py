from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.models.projects import Project
from src.schemas.projects import ProjectSchema


class ProjectService:
    @staticmethod
    async def search_projects(query: str) -> list[ProjectSchema]:
        async with AsyncClient() as client:
            response = await client.get(
                f"https://gitlab.com/api/v4/projects/?search={query}"
            )
            projects = response.json()

            results = [
                ProjectSchema(
                    id=project["id"],
                    name=project["name"],
                    description=project["description"],
                    last_activity=project["last_activity_at"],
                )
                for project in projects
            ]
            return results

    @staticmethod
    async def save_projects(
        session: AsyncSession, projects: list[ProjectSchema], query: str
    ):
        insert_projects = [Project(**data.model_dump()) for data in projects]

        get_projects_query = select(Project).where(Project.name.ilike(f"%{query}%"))

        try:
            session.add_all(insert_projects)
            await session.commit()

            projects = await session.execute(get_projects_query)

            return projects.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting projects from DB: {e.args}")
