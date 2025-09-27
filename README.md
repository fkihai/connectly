# IoT Platform (FastAPI + PostgreSQL)

A simple IoT management platform built with **FastAPI**.
This platform will handle:

- **User authentication** (login, register)
- **Device management** (add, list, update, delete IoT devices)
- **Data storage** (store sensor data from devices)
- **REST API** for clients or IoT devices

---

## Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Auth**: JWT (Json Web Token)
- **Deployment**: Uvicorn
- **Migration**: Alembic

---

## Installation & Setup (with Poetry)

```bash
# Clone the repository
git clone https://github.com/fkihai/connectly.git
cd connectly

# Install dependencies
poetry install

# Run database migrations
poetry run alembic upgrade head

# Start the server
poetry run uvicorn app.main:app --reload
```

---

## Database Migration (Alembic)

```bash
# Generate a new migration
alembic revision --autogenerate -m "{message}"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

---
