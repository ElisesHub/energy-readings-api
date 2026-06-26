# Energy Readings API

A FastAPI service for ingesting and querying hourly energy meter readings, built while broadening my stack into Python and data engineering.

> **Status:** Five endpoints implemented (GET /readings, GET /readings/{id}, POST /readings, POST /readings/bulk, GET /aggregates/daily). Tests are the next addition.

## Tech stack

Python 3.14 · FastAPI · SQLModel · PostgreSQL 18 · Docker Compose

## Structure

I organised this project by feature (vertical slice), and then organised each feature by CQS — command/query separation. This is more structure than a service this small strictly needs, but I appreciate well-organised code that's pleasant to work with, and the cost of vertical slices at small scale is essentially zero. Clean Architecture would have been overkill — the project isn't going to scale, and layer-jumping between core, application, infrastructure, and presentation would add noise without paying back. Vertical slice with CQS (not full CQRS with separate models, because the system doesn't need read/write divergence) gives a clean, navigable layout where any features I add later stay self-contained and easy to maintain.

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

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/readings` | List readings. Filters: `meter_id`, `reading_type`, `from`, `to`. Paginated. |
| `GET` | `/readings/{id}` | Fetch one reading. 404 if missing. |
| `POST` | `/readings` | Create a single reading. |
| `POST` | `/readings/bulk` | Bulk-create readings from a JSON array. |
| `GET` | `/aggregates/daily` | Daily kWh totals per meter, filtered by date range and reading type. |
 
 
### Using a terminal:
```bash
# All readings (default pagination)
curl "http://localhost:8000/readings" | jq

# Filtered by meter, type, and date range
curl "http://localhost:8000/readings?from=2025-12-01T00:00:00&to=2026-06-30T23:59:59&limit=20" | jq

# Wider date range to see more results across meters:
curl "http://localhost:8000/readings?from=2025-12-01T00:00:00&to=2026-06-30T23:59:59&limit=20" | jq

# One meter only, full range:
curl "http://localhost:8000/readings?meter_id=SEC-GM-1234567&from=2025-12-01T00:00:00&to=2026-06-30T23:59:59" | jq

# Generation only
curl "http://localhost:8000/readings?reading_type=generation&from=2026-01-01T00:00:00&to=2026-05-01T00:00:00&limit=15" | jq

# Single reading by ID
curl "http://localhost:8000/readings/1" | jq

# Create a single reading
curl -X 'POST'  'http://localhost:8000/readings' -H 'accept: application/json'  -H 'Content-Type: application/json'  -d '{
  "meter_id": "NEW-81B-29766789",
  "timestamp": "2026-01-19T12:32:21.972Z",
  "kwh": 18.2,
  "reading_type": "consumption"
}'

# Bulk import readings 
# NOTE >> this example deliberately includes a duplicate to demonstrate bulk-insert handling
curl -X 'POST'  'http://localhost:8000/readings/bulk' -H 'accept: application/json'  -H 'Content-Type: application/json'  -d '[
  {
    "meter_id": "meter-200",
    "timestamp": "2026-06-19T12:12:29.154Z",
    "kwh": 1.2,
    "reading_type": "consumption"
  },
{
    "meter_id": "meter-200",
    "timestamp": "2026-06-19T12:12:29.154Z",
    "kwh": 2.5,
    "reading_type": "generation"
  },
{
    "meter_id": "meter-201",
    "timestamp": "2026-06-19T12:12:29.154Z",
    "kwh": 1.2,
    "reading_type": "consumption"
  },
{
    "meter_id": "meter-201",
    "timestamp": "2026-06-19T12:12:29.154Z",
    "kwh": 1.2,
    "reading_type": "consumption"
  }
]' | jq
```
### Using a browser:
Please go to http://localhost:8000/docs to see swagger documentation and try any endpoint. 

For GET requests, you can enter the URLs into your browser very easily, for example:
```
# All readings (default pagination)
http://localhost:8000/readings

# Filtered by meter, type, and date range
http://localhost:8000/readings?meter_id=LGY-19A-12345678&reading_type=consumption&from=2025-12-01T00:00:00&to=2026-03-01T00:00:00&limit=50

# Single reading by ID
http://localhost:8000/readings/1
```


## Tests

Tests live alongside the code they test — each vertical slice owns its own test files (e.g. `app/energy_readings/queries/list_readings/tests/`). Pytest discovers them automatically from a single `conftest.py` at the project root, which provides a `db_session` fixture (transaction-per-test, rolled back on teardown) and an `http_client` fixture (FastAPI's `TestClient` with the test database wired in via dependency override).

### Getting started with the tests

**1. Start the test database** (separate from the main app database, runs on a different port):

```bash
docker compose --env-file .env.test -f docker-compose.test.yml up -d
```

**2. Run the tests:**

```bash
pytest                                  # all tests
pytest -v                               # verbose output
pytest path/to/test_file.py             # one file
pytest path/to/test_file.py::test_name  # one test
```

Or in your IDE — both PyCharm and VS Code support running individual tests or whole files by clicking the green arrow in the gutter (PyCharm) or the test runner icon (VS Code), provided pytest is set as the default test runner in settings.

**3. Stop the test database when finished:**

```bash
docker compose --env-file .env.test -f docker-compose.test.yml down
```

Add `-v` to wipe the volume and force the init SQL scripts to re-run on the next startup.


 