import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# Drop the existing table
cursor.execute("DROP TABLE IF EXISTS tasks")

# Create the new table with 'status' column
cursor.execute("""
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'todo'
    )
""")

conn.commit()
conn.close()
