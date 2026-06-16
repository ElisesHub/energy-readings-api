# Energy Readings API

A FastAPI + PostgreSQL service for ingesting and reporting energy meter consumption and generation readings. Built with vertical slice architecture and a CQRS-style command/query split, containerized with Docker.

## Tech Stack

- **Python 3.13**
- **FastAPI** — web framework
- **SQLModel** — ORM (SQLAlchemy + Pydantic combined)
- **PostgreSQL 16** — database
- **Pydantic Settings** — typed configuration management
- **Docker / Docker Compose** — containerization and local orchestration

## Architecture

The codebase is organized by feature, not by technical layer:

- **Vertical slice architecture** — each use case (e.g. `get_data_reports`) owns its own router, repository, schemas, and service, rather than spreading related code across global `routes/`, `models/`, `services/` folders.
- **CQRS-style split** — top-level `commands/` and `queries/` folders separate write operations from read operations.
- **Repository pattern** — data access is abstracted behind repository classes, constructor-injected with a database session via FastAPI's `Depends()`.
- **Shared domain layer** — entities and enums used across multiple slices within a feature live in that feature's `shared/` folder.

```
energy-readings-api/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── init/
│   ├── 01-create-tables.sql
│   └── 02-seed-data.sql
└── app/
    ├── main.py
    ├── shared/
    │   └── infrastructure/
    │       ├── settings.py
    │       └── database.py
    └── energy_readings/
        ├── commands/
        │   ├── ingest_data_from_file/
        │   └── insert_single/
        ├── queries/
        │   └── get_data_reports/
        │       ├── repository.py
        │       ├── routers.py
        │       ├── schemas.py
        │       └── service.py
        └── shared/
            ├── energy_reading.py
            └── energy_reading_type.py
```

## Getting Started

### Prerequisites

- Docker Desktop

### Setup

1. Clone the repository.
2. Copy the example environment file and fill in real values:
   ```bash
   cp .env.example .env
   ```
3. Build and start the stack:
   ```bash
   docker compose up --build
   ```
4. The API is available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

On first startup, Postgres automatically creates the database and runs the scripts in `init/`, creating the schema and inserting seed data. This only happens once, against a fresh volume — to reset the database to a clean state later, run `docker compose down -v` before starting again.

### Running Natively (for debugging)

To debug the app directly rather than inside the container:

1. Start only Postgres: `docker compose up postgres`
2. Install dependencies into a local virtual environment: `pip install -r requirements.txt`
3. Run the app with `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`

The app's default settings (`localhost`, the published Postgres port) are already configured for this native scenario — no extra setup needed beyond having Postgres running.

## Environment Variables

See `.env.example` for the full list. Required:

| Variable | Description |
|---|---|
| `POSTGRES_USERNAME` | Postgres role used by the app and by Postgres itself on init |
| `POSTGRES_PASSWORD` | Password for that role |
| `DB_REF` | Name of the database to create and connect to |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/reports` | Returns all energy readings |

Full interactive documentation is available at `/docs` once the app is running.

## Database Schema

**`energy_reading`**

| Column | Type | Notes |
|---|---|---|
| `id` | `SERIAL` | Primary key |
| `meter_id` | `VARCHAR` | Identifier of the originating meter |
| `timestamp` | `TIMESTAMPTZ` | When the reading was recorded |
| `age` | `DOUBLE PRECISION` | Nullable |
| `reading_type` | `VARCHAR` | Constrained to `consumption` or `generation` |