from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_async_session
from app.tasks.dao import TaskDAO
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_session)
):
    new_task = Task(**task.model_dump(), owner_id = 1)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[TaskRead])
async def get_tasks(db: AsyncSession = Depends(get_async_session)):
    return await TaskDAO.get_all(db)

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    task = await TaskDAO.get_by_id(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    updated: TaskUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    task = await TaskDAO.update(task_id, updated.model_dump(exclude_unset=True), db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task