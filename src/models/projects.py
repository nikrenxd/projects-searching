from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    last_activity: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
