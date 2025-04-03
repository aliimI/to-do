from datetime import datetime
from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Task

class TaskDAO:

    @staticmethod
    async def get_all_by_owner(
        owner_id: int, 
        db: AsyncSession,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        search: Optional[str] = None
        ) -> list[Task]:

        query = select(Task).where(Task.owner_id == owner_id)

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if due_before:
            query = query.where(Task.due_date <= due_before)
        if due_after:
            query = query.where(Task.due_date >= due_after)
        if search:
            search_pattern = f"%{search.lower()}%"
            query = query.where(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern)
                )
            )

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(task_id: int, db: AsyncSession) -> Optional[Task]:
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(task_data: dict, db: AsyncSession) -> Task:
        task = Task(**task_data)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete(task_id: int, db: AsyncSession) -> bool:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()

        if not task: 
            return False
        
        await db.delete(task)
        await db.commit()
        return True

    @staticmethod
    async def update(task_id: int, data: dict, db: AsyncSession) -> Optional[Task]:
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return None
        
        for k, v in data.items():
            if v is not None:
                setattr(task, k, v)

        await db.commit()
        await db.refresh(task)
        return task
    
