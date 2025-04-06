from sqladmin import Admin, ModelView
from app.tasks.models import Task
from app.users.models import User

class UsersAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.created_at]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class TasksAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.title, Task.description, Task.owner] 
    column_details_exclude_list = [Task.created_at, Task.updated_at]
    
    name = "Task"
    name_plural = "Tasks"
    icon = "fa-solid fa-list"

