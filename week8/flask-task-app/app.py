from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        deadline = request.form["deadline"]

        if not title:
            return "Title is required"

        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title, description, deadline, created_at) VALUES (?, ?, ?, ?)",
            (title, description, deadline, datetime.now()),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        deadline = request.form["deadline"]
        status = request.form["status"]

        conn.execute(
            "UPDATE tasks SET title=?, description=?, deadline=?, status=? WHERE id=?",
            (title, description, deadline, status, id),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("edit.html", task=task)


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)