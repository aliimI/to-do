from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_async_session
from app.tasks.dao import TaskDAO
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskRead, TaskUpdate
from app.auth.deps import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)



@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(**task.model_dump(), owner_id = current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=list[TaskRead])
async def get_tasks(db: AsyncSession = Depends(get_async_session), 
                    current_user: User = Depends(get_current_user)):
    return await TaskDAO.get_all_by_owner(current_user.id, db)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, 
                   db: AsyncSession = Depends(get_async_session),
                   current_user: User = Depends(get_current_user)):
    task = await TaskDAO.get_by_id(task_id, db)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    updated: TaskUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    task = await TaskDAO.get_by_id(task_id, db)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_data = updated.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        if value is not None:
            setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, 
                      db: AsyncSession = Depends(get_async_session),
                      current_user: User = Depends(get_current_user)):
    task = await TaskDAO.get_by_id(task_id, db)

    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return None