from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Task

class TaskDAO:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Task]:
        result = await db.execute(select(Task))
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
    async def delete(task: Task, db: AsyncSession):
        await db.delete(task)
        await db.commit()

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