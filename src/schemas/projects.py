from datetime import datetime

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: str | None
    last_activity: datetime
