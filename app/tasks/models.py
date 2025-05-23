from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.sql import expression
from datetime import datetime, timezone
from typing import Optional
from app.users.models import User
from app.tasks.schemas import Repeat
from enum import Enum



class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="To-Do")
    priority: Mapped[str] = mapped_column(String, default="Medium")
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    repeat: Mapped[Repeat] = mapped_column(
        String, default=Repeat.none, 
        # server_default=expression.literal_column("'None'"), 
        nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="tasks", lazy="selectin")

    