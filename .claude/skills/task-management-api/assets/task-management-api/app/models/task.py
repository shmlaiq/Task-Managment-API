"""Task model definitions using SQLModel."""

from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(SQLModel):
    """Base Task model with shared fields."""
    title: str = Field(index=True)
    description: str | None = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = None


class Task(TaskBase, table=True):
    """Task database model."""
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskRead(TaskBase):
    """Schema for reading a task."""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating a task (all fields optional)."""
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
