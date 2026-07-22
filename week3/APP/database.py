import sqlite3
from contextlib import contextmanager

DB_FILE = "tasks.db"


class Database:
    def connect_to_db(self, db_file: str = DB_FILE):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        # row_factory lets fetch* calls come back as dict-like Row objects
        # instead of bare tuples, so main.py can do row["title"] / dict(row).
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        print("Connected to tasks.db ....")

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )
        self.conn.commit()

    def seed(self):
        """Insert 3 example tasks, but only the first time the table is empty."""
        self.cur.execute("SELECT COUNT(*) FROM tasks")
        (count,) = self.cur.fetchone()
        if count == 0:
            self.cur.execute("BEGIN")
            try:
                self.cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (?, ?)",
                    [
                        ("Buy milk", False),
                        ("Read chapter 3", False),
                        ("Push A1 to GitHub", True),
                    ],
                )
                self.conn.commit()
            except Exception:
                self.conn.rollback()
                raise
            print("Seeded 3 example tasks.")

    # ---- CRUD -----------------------------------------------------------

    def add(self, title: str, done: bool = False):
        self.cur.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title, done),
        )
        self.conn.commit()
        return self.read(self.cur.lastrowid)

    def read_all(self, search: str | None = None, done: bool | None = None):
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list = []
        if search:
            query += " AND title LIKE ?"
            params.append(f"%{search}%")
        if done is not None:
            query += " AND done = ?"
            params.append(done)
        self.cur.execute(query, params)
        return [dict(row) for row in self.cur.fetchall()]

    def stats(self):
        self.cur.execute(
            "SELECT COUNT(*) AS total, SUM(done) AS done FROM tasks"
        )
        row = self.cur.fetchone()
        total = row["total"] or 0
        done = row["done"] or 0
        return {"total": total, "done": done, "pending": total - done}

    def read(self, id: int):
        self.cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        row = self.cur.fetchone()
        return dict(row) if row else None

    def update(self, id: int, title: str, done: bool):
        self.cur.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (title, done, id),
        )
        self.conn.commit()
        if self.cur.rowcount == 0:
            return None
        return self.read(id)

    def delete(self, id: int) -> bool:
        self.cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
        self.conn.commit()
        return self.cur.rowcount > 0

    def close(self):
        print("Connection closed....")
        self.conn.close()


# usage as a context manager, e.g.:
#   with managed_db() as db:
#       db.read_all()
@contextmanager
def managed_db():
    db = Database()
    print("Enter Setup ...")
    db.connect_to_db()
    db.create_table()
    db.seed()
    try:
        yield db
    finally:
        db.close()
