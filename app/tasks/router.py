from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_async_session
from app.tasks.dao import TaskDAO
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskRead, TaskUpdate
from app.auth.deps import get_current_user
from app.users.models import User
from app.tasks.schemas import Status, Priority
from app.background.email_jobs import send_due_reminder


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

def get_reminder_offset(priority: str) -> timedelta:
    #for python > 3.10
    # match priority:
    #     case "High":
    #         return timedelta(days=1)
    #     case "Medium":
    #         return timedelta(hours=6)
    #     case "Low":
    #         return timedelta(hours=1)
    #     case _:
    #         return timedelta(hours=1)
    if priority == "High":
        return timedelta(days=1)
    elif priority == "Medium":
        return timedelta(hours=6)
    elif priority == "Low":
        return timedelta(hours=1)
    else:
        return timedelta(hours=1)
    

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


    #reminder functionality 
    if new_task.due_date:
        reminder_eta = new_task.due_date - get_reminder_offset(new_task.priority)
        # #testing 
        # reminder_eta = datetime.now(timezone.utc) + timedelta(seconds=30)

        if reminder_eta > datetime.now(timezone.utc):
            send_due_reminder.apply_async(
                args=[new_task.title, current_user.email, new_task.due_date.isoformat()],
                eta=reminder_eta
            )
        else:
            print("Reminder time is in the past")

    return new_task


@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    status: Optional[Status] = None, 
    priority: Optional[Priority] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session), 
    current_user: User = Depends(get_current_user)
    ):

    return await TaskDAO.get_all_by_owner(
        owner_id=current_user.id,
        db=db,
        status=status,
        priority=priority,
        due_before=due_before,
        due_after=due_after,
        search=search
    )


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