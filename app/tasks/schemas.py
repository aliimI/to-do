from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class Status(str, Enum):
    todo = "To-Do"
    in_progress = "In Progress"
    done = "Done"

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class Repeat(str, Enum):
    none = "None"
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status
    priority: Priority
    due_date: Optional[datetime] = None
    repeat: Repeat = Repeat.none
    

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None

class TaskRead(TaskCreate):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


