from fastapi import FastAPI
from app.tasks.models import Task
from app.users.models import User
from app.users.router import router as user_router
from app.tasks.router import router as task_router
from app.auth.router import router as auth_router
from app.admin.views import UsersAdmin, TasksAdmin

from sqladmin import Admin, ModelView
from app.database import engine

app = FastAPI()

app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "FastAPI To-Do List app is running"}

admin = Admin(app, engine)




admin.add_view(UsersAdmin)
admin.add_view(TasksAdmin)
