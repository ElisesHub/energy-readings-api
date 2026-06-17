# Energy Readings API

A FastAPI service for ingesting and querying hourly energy meter readings, built as part of my move from C#/.NET into Python and data engineering.

> **Status:** work in progress. `GET /readings`, `GET /readings/{id}` working; `POST /readings`, `POST /readings/bulk`, `GET /aggregates/daily` and tests still to come.

## Tech stack

Python 3.14 · FastAPI · SQLModel · PostgreSQL 16 · Docker Compose

## Architecture

Organised by feature rather than by technical layer.

- **Vertical slice architecture** — each use case (e.g. `list_readings`) owns its router, handler, and schemas in one folder.
- **CQRS split** — top-level `commands/` and `queries/` separate writes from reads. Reads project directly into Pydantic response models; no read-side repository.
- **Shared domain** in `energy_readings/shared/` (entity, enum). Infrastructure (DB session, settings) in `app/shared/infrastructure/`.

## Run

```bash
cp .env.example .env       # safe local defaults are pre-filled
docker compose up --build
```

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

To reset the database (init SQL only runs on a fresh volume):

```bash
docker compose down -v && docker compose up --build
```

## API (so far)

| Method | Path | Description |
|---|---|---|
| `GET` | `/readings` | List readings. Filters: `meter_id`, `reading_type`, `from`, `to`. Paginated. |
| `GET` | `/readings/{id}` | Fetch one reading. 404 if missing. |
 
```bash
# All readings (default pagination)
curl "http://localhost:8000/readings" | jq

# Filtered by meter, type, and date range
curl "http://localhost:8000/readings?meter_id=meter-001&reading_type=consumption&from=2024-01-01T00:00:00&to=2026-03-01T00:00:00&limit=50" | jq

# Single reading by ID
curl "http://localhost:8000/readings/1" | jq
 
```