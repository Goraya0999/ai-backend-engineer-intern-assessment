# Task API — SQLite edition (W3 · A2)

A CRUD task API (FastAPI, Python lane) backed by SQLite instead of an
in-memory list. Same endpoints, same request/response shapes as A1 —
only the storage layer changed.

## Run it

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

On first run this creates `tasks.db` in the project folder, creates the
`tasks` table if it doesn't exist, and seeds 3 example tasks — but only
if the table is empty, so restarting never duplicates them.

## Why SQLite

- Zero setup: no separate database server to install or run, no
  connection string, no Docker container.
- Single file (`tasks.db`): easy to inspect, back up, or delete to reset.
- Enough for a project this size, and the exact same SQL (`SELECT`,
  `INSERT`, `WHERE`, parameterized `?` placeholders) carries over
  directly to Postgres/MySQL later — only the driver changes.

`tasks.db` is git-ignored, so every fresh clone starts with a clean,
auto-seeded database.

## Endpoints

| Method | Path          | Behaviour                                  |
|--------|---------------|---------------------------------------------|
| GET    | /tasks        | list tasks (`?search=`, `?done=` optional)  |
| GET    | /tasks/{id}   | one task, 404 if unknown                    |
| POST   | /tasks        | create, 400 if title missing/empty, 201 ok  |
| PUT    | /tasks/{id}   | update title+done, 404 if unknown           |
| DELETE | /tasks/{id}   | delete, 404 if unknown, 204 on success      |
| GET    | /stats        | `{total, done, pending}` via SQL `COUNT()`  |

All CRUD operations use parameterized queries (`?` placeholders) — no
user input is ever glued into a SQL string.

## Example SQL query I ran in DB Browser (Stage 4)

```sql
SELECT * FROM tasks WHERE done = 1;
```
Returned the one seeded task ("Push A1 to GitHub") that starts out
marked done — confirms the API and DB Browser are reading the exact
same file, with no syncing step in between.

## Screenshot

_(add your DB Browser screenshot here before pushing — Stage 5 requirement)_
