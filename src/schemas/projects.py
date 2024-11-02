from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    description: str | None
    last_activity: datetime
