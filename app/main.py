from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
)

@app.get("/")
async def root():
    return {"message": "FastAPI To-Do List app is running"}

admin = Admin(app, engine)




admin.add_view(UsersAdmin)
admin.add_view(TasksAdmin)
