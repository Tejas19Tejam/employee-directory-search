# Employee Directory Search System

A small internal tool to search and view employees by name or department.

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Python + FastAPI
- **Database:** MySQL

```
project-2/
├── backend/   # FastAPI service, MySQL access, search API
├── frontend/  # React + Vite + Tailwind UI

```

## Setup Steps

### 1. Database (MySQL)

Create the database and table. You can either let the seed script do it
automatically, or run the DDL yourself:

```sql
-- backend/schema.sql
CREATE DATABASE IF NOT EXISTS employee_directory
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
# edit .env with your MySQL credentials

# creates the employees table (if missing) and inserts sample data
python -m app.db.seed

# run the API
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at
`http://localhost:8000/docs`.

### 3. Frontend

```powershell
cd frontend
npm install

Copy-Item .env.example .env
# edit .env if your backend runs somewhere other than http://localhost:8000

npm run dev
```

The app will be available at `http://localhost:5173`.

## Database Choice

**MySQL**, as requested in the brief, accessed through SQLAlchemy's ORM
(`PyMySQL` driver).

- The data is tabular and fixed-shape (id, name, email, department,
  designation, date_of_joining) with no need for nested documents or
  flexible schemas, which fits a relational database better than a
  document store.
- Search is filter-based (`WHERE name LIKE ... OR department LIKE ...`),
  which is exactly what a relational engine with B-tree indexes is built
  to do efficiently.
- SQLAlchemy gives a connection **pool** (`QueuePool`) instead of opening a
  new TCP connection per request, with `pool_pre_ping` to transparently
  recover from dropped idle connections, and pool size/overflow/recycle
  all driven by environment variables so the same code scales from a
  laptop to a production instance without code changes.
- The ORM also keeps SQL out of the route handlers; queries are built with
  the query builder in a single repository class, which is easy to read,
  extend, and (if ever needed) swap for raw SQL/another DB.

## How Search Performance Is Optimized (Conceptually)

**Frontend side — fewer requests:**
- The search input value is **debounced** (`useDebouncedValue`, 400ms). The
  API is only called once typing pauses, so typing "Rah" quickly sends one
  request for "Rah" instead of three requests for "R", "Ra", "Rah".
- Each new request **aborts the previous in-flight request** via
  `AbortController`. This avoids wasted backend work and prevents a slow,
  stale response from a previous keystroke from overwriting newer results
  (a race condition).

**Backend side — cheap, scalable queries:**
- `name` and `department` each have a **dedicated index**
  (`ix_employees_name`, `ix_employees_department`), so filtering by either
  column stays fast as the table grows, instead of degrading into a full
  table scan.
- The search endpoint is **paginated** (`limit`/`offset`, capped at 100 per
  page). Only the requested page is fetched from MySQL — the API never
  loads the entire table into memory just to filter or count it.
- The total result count is a single `COUNT(*)` query reusing the same
  `WHERE` filter, not a count of an already-fetched Python list.
- Response payloads only include the columns the frontend actually needs
  (no over-fetching).

## API

`GET /employees?search=<term>&limit=<n>&offset=<n>`

| Param  | Required | Notes                                             |
|--------|----------|----------------------------------------------------|
| search | no       | Matched against `name` OR `department` (case-insensitive, substring). Rejected if present but blank/whitespace. |
| limit  | no       | Default 20, max 100.                                |
| offset | no       | Default 0.                                          |

Responses:
- `200` — `{ items: Employee[], total, limit, offset }`
- `422` — invalid query params (e.g. empty search, out-of-range limit/offset)
- `503` — database unreachable
- `500` — unexpected server error (generic message, no stack trace leaked)

`GET /health` — liveness check, returns `{ "status": "ok" }`.

## Backend Architecture

```
app/
├── main.py                        # FastAPI app, CORS, global exception handler
├── core/config.py                 # env-based settings (pydantic-settings)
├── db/session.py                  # SQLAlchemy engine, connection pool, get_db dependency
├── db/seed.py                     # creates tables + inserts sample employees
├── models/employee.py             # ORM model + indexes
├── schemas/employee.py            # Pydantic request/response schemas
├── repositories/employee_repository.py   # DB access only, no business logic
├── services/employee_service.py          # validation + business rules
└── routers/employees.py                  # HTTP layer, thin route handlers
```

Each layer has one job: routers handle HTTP, services hold business rules
and validation, repositories talk to the database. This keeps route
handlers thin and makes it straightforward to add new features (e.g. an
endpoint to create employees) without touching unrelated layers.

## Frontend Architecture

```
src/
├── config.js                      # reads VITE_API_BASE_URL
├── api/employeeApi.js             # all fetch/network logic, ApiError type
├── hooks/useDebouncedValue.js      # generic debounce hook
├── hooks/useEmployeeSearch.js      # search state machine (loading/success/error), abort handling
└── components/
    ├── SearchBar.jsx               # presentational input
    ├── EmployeeCard.jsx            # presentational employee row
    ├── EmployeeList.jsx            # chooses loading/empty/error/results view
    └── StatusStates.jsx            # Loading / Empty / Error presentational states
```

UI components receive data and callbacks as props and contain no API calls;
all fetching and state management for the search feature lives in
`useEmployeeSearch`.

## Environment Variables

Neither project hardcodes URLs or credentials — see `backend/.env.example`
and `frontend/.env.example`.

**backend/.env**
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=employee_directory
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
CORS_ORIGINS=http://localhost:5173
APP_ENV=development
```

**frontend/.env**
```
VITE_API_BASE_URL=http://localhost:8000
```
