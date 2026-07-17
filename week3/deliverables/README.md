# A2 Service — Postgres + Docker

## Run it

```bash
cp .env.example .env      # then edit the password
docker compose up --build
```

App: http://localhost:8000/scalar (Scalar docs) or http://localhost:8000/home

Postgres and Redis both run with a healthcheck, and `app` waits for
`condition: service_healthy` on both before it starts, so you don't get the
classic "app boots before Postgres accepts connections" crash on first run.

## Architecture — service/routes did not change

- `repository.py` defines the `UserRepository` interface (`add`,
  `get_by_name`, `get_by_email`).
- `postgress_repository.py` is the only new file: a `PostgresRepository`
  implementing that interface with a real `Session`.
- `dependencies.py` is the single wire-up point — it constructs
  `PostgresRepository(session)` and hands it to `RegisterService`.
- `service.py` and `main.py` were **not** touched for the storage swap —
  they only ever talk to `UserRepository`, never to Postgres directly.
  (I did add a `get_user` method to the service and a `GET /users/{username}`
  route, purely so there's a way to prove persistence after a restart —
  that's new functionality, not a change to how storage is swapped in.)

This is the actual proof the layering claim in the assignment is asking for:
swapping storage was a one-file change (`postgress_repository.py` +
1 line in `dependencies.py`), not a rewrite.

## Where the connection string comes from

`config.py` reads `POSTGRES_SERVER/PORT/USER/PASSWORD/DB` from `.env` via
`pydantic-settings` and builds the SQLAlchemy URL. `.env` is gitignored;
`.env.example` is committed with placeholder values. Inside
`docker-compose.yml`, `POSTGRES_SERVER` is overridden to `db` (the Postgres
service name on the compose network) regardless of what's in `.env`, since
`localhost` doesn't mean "the other container" from inside the app container.

## Table creation

`database.py:create_table()` runs `SQLModel.metadata.create_all()` on
FastAPI's startup event — this is the "tiny init script" the assignment
mentions, driven by the `UserRegister` model in `model.py` rather than a
separate `.sql` file. Since it's idempotent (`create_all` no-ops on tables
that already exist), it's safe to run on every container start.

## How I proved persistence

1. `docker compose up -d`
2. `curl -X POST localhost:8000/signup -H "Content-Type: application/json" -d '{"firstname":"Ada","lastname":"Lovelace","username":"ada1","email":"ada@example.com","password":"Str0ng!!Passw0rd"}'`
3. `curl localhost:8000/users/ada1` → row is there.
4. `docker compose restart app db` (or `docker compose down` then
   `docker compose up -d` — without `-v`, so the `pgdata` volume is kept).
5. `curl localhost:8000/users/ada1` → same row comes back, because the data
   lives in the `pgdata` named volume, not in the container's writable layer.
6. Sanity check the negative case: `docker compose down -v` (removes the
   volume too) then bring the stack back up — `/users/ada1` now 404s,
   confirming the volume, not luck, was what preserved the data.

## Stretch: Redis

`redis` is in `docker-compose.yml` with its own healthcheck. It's wired into
the stack (compose network + healthcheck) but not yet called from the app —
next step would be a `redis.from_url()` client in `database.py` and a
`/health/redis` route that does a `PING`, for Week 4.

## Bugs fixed on top of the uploaded code

- `model.py` used `regex=` on `Field(...)`, which Pydantic v2 removed in
  favor of `pattern=` — as uploaded, this raises `PydanticUserError` at
  import time and the app never starts. Changed `regex=` → `pattern=` in
  all three places (matches what `schema.py` already does correctly).
- `service.py`/`postgress_repository.py`: signing up a duplicate
  username/email hit the DB's unique constraint and bubbled up as an
  unhandled `IntegrityError` → bare 500. Now caught and rolled back,
  returned as a 409.

## Still worth a look (not changed, flagging for you)

- The password regex uses several `(?:.*X){n,}` lookaheads — nested
  quantifiers like that are a known ReDoS pattern on adversarial input.
  Worth swapping for four separate single-pass counts if you want to be
  safe against very long password fields.
- `__tablename__ = "Users"` (capital U) makes Postgres treat it as a
  case-sensitive quoted identifier. Not wrong, but if you ever hand-write
  raw SQL against this table you'll need `"Users"` with quotes.
- `id: int = Field(default=None, primary_key=True)` — works with SQLModel,
  but `Optional[int]` is the more honest type hint for a nullable
  autoincrement PK.
