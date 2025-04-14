from .worker import celery_app
from app.tasks.models import Task, Repeat
from app.database import async_session_maker
from sqlalchemy import select

from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

@celery_app.task
def repeat_tasks():
    print("running repeat task job...")

    async def inner():
        async with async_session_maker() as session:
            now = datetime.now(timezone.utc)

            result = await session.execute(
                select(Task).where(
                    Task.repeat != Repeat.none,
                    Task.due_date <= now
                )
            )
            tasks = result.scalars().all()

            for task in tasks:
                new_due = None
                if task.repeat == Repeat.daily:
                    new_due = task.due_date + timedelta(days=1)
                elif task.repeat == Repeat.weekly:
                    new_due = task.due_date + timedelta(weeks=1)
                elif task.repeat == Repeat.monthly:
                    new_due = task.due_date + relativedelta(months=1)

                if new_due:
                    new_task = Task(
                        title=task.title,
                        description=task.description,
                        status="To-Do",
                        priority=task.priority,
                        due_date=new_due,
                        repeat=task.repeat,
                        owner_id=task.owner_id,
                    )
                    session.add(new_task)
                    print(f"New Repeating task was created: {new_task.title} for {new_due}")

            await session.commit()
    
    import asyncio
    asyncio.run(inner())