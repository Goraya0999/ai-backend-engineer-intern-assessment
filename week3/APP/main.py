from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from database import Database
from schema import CreateTask, ReadTask, UpdateTask

db = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Stage 0: create tasks.db + tasks table if missing, seed 3 example
    # rows only the first time the table is empty.
    db.connect_to_db()
    db.create_table()
    db.seed()
    yield
    db.close()


app = FastAPI(title="Task Api", lifespan=lifespan)


# Assignment requires 400 (not FastAPI's default 422) for bad request bodies,
# e.g. a missing/empty title. This converts pydantic validation failures into
# the { "error": ... } / 400 shape used everywhere else in the API.
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


# List all tasks — optional extras: ?search=, ?done=
@app.get("/tasks", response_model=list[ReadTask])
def get_tasks(search: str | None = None, done: bool | None = None):
    return db.read_all(search=search, done=done)


# Optional extra: stats computed with SQL COUNT(), not Python
@app.get("/stats")
def get_stats():
    return db.stats()


# Get a single task by id
@app.get("/tasks/{id}", response_model=ReadTask)
def get_task(id: int):
    task = db.read(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Create a new task
@app.post("/tasks", response_model=ReadTask, status_code=201)
def submit_task(task: CreateTask):
    return db.add(task.title, task.done)


# Update an existing task (full replace of title + done)
@app.put("/tasks/{id}", response_model=ReadTask)
def update_task(id: int, task: UpdateTask):
    updated = db.update(id, task.title, task.done)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


# Delete a task
@app.delete("/tasks/{id}", status_code=204)
def del_task(id: int):
    deleted = db.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


# HTTPException already returns {"detail": ...}; the spec wants {"error": ...}
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
