from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.projects import ProjectSchema
from src.services.projects import ProjectService

pytestmark = pytest.mark.anyio


class TestProjectsService:
    async def test_search_projects(self):
        projects = await ProjectService.search_projects(query="Django")

        assert projects

    async def test_save_project(self, session: AsyncSession):
        project = await ProjectService.save_projects(
            session,
            projects=[
                ProjectSchema(
                    id=123,
                    name="project1",
                    description=None,
                    last_activity=datetime.now(),
                ),
            ],
            query="project1",
        )

        assert project[0].name == "project1"
