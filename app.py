from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    # Group tasks by status
    tasks_by_status = {"todo": [], "in_progress": [], "done": []}
    for task in tasks:
        tasks_by_status[task["status"]].append(task)

    return render_template("index.html", tasks=tasks_by_status)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]
    status = request.form.get("status", "todo")  # Default to 'todo'
    if task:
        conn = get_db_connection()
        conn.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, status))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/update_status", methods=["POST"])
def update_status():
    task_id = request.form["task_id"]
    new_status = request.form["new_status"]

    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated successfully!"})

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
