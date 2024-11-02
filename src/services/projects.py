from httpx import AsyncClient

from src.schemas.projects import Project


class ProjectService:
    @staticmethod
    async def search_projects(query: str):
        async with AsyncClient() as client:
            response = await client.get(
                f"https://gitlab.com/api/v4/projects/?search={query}"
            )
            projects = response.json()

            results = [
                Project(
                    id=project["id"],
                    name=project["name"],
                    description=project["description"],
                    last_activity=project["last_activity_at"],
                )
                for project in projects
            ]

            return results
