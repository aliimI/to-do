# To-do App
FastAPI To-Do App with delayed tasks

Full-featured backend part for To-Do list app built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**:
- JWT-based authentication
- Task management with priority, due date, and repeat logic
- Automated email reminders (Celery + Redis)
- Admin panel (SQLAdmin)
- Async database access with SQLAlchemy
- Background tasks with support for repeating tasks

## Features
- User Registration / Login
- JWT Tokens 
- CRUD
- Task repeat logic (`None`, `Daily`, `Weekly`, `Monthly`)
- Celery job to auto-repeat tasks based on schedule
- Email reminders via Gmail SMTP
- Admin panel for managing Users & Tasks

