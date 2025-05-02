# To-Do App - FastAPI Backend

A full-featured asynchronous To-Do app backend built with **FastAPI**, **PostgreSQL**, **Celery**, and **Redis**, featuring:
- JWT based user authentication
- Task management with priorities, due dates, and repeat schedules
- Automated email reminders
- Admin panel for managing users and tasks
- Background task support (auto-repeat logic)

## Features
- User Registration and Login (JWT Auth)
- CRUD for tasks 
- Task repeat logic: None, Daily, Weekly, Monthly
- Delayed tasks with Celery + Redis
- Email reminders via Gmail SMTP
- Admin panel using SQLAdmin
- Async PostgreSQL access with SQLAlchemy
  
## Tech Stack

| Tool  | Purpose |
| ------------- | ------------- |
| FastAPI  | Web framework  |
| SQLAlchemy  | Async ORM  |
| PostgreSQL | Database |
| Alembic | DB migrations |
| Celery | Background job |
| Redis | Message broker for Celery |
| SQLAdmin | Admin panel |
| Pydantic | Validation |
| Vue 3 | Frontend framework |
| Vite | Frontend build tool |

