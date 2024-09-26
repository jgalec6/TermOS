import sqlite3


def create_users_table():
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    # Create the user table if doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT NOT NULL)
    """)

    # Check if the "admin" already exists
    cur.execute("SELECT * FROM users WHERE username = 'admin'")
    admin_exists = cur.fetchone()
    if not admin_exists:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "passwd")
        )

    con.commit()
    con.close()


def validate_login(username, password):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (
            username, password)
    )
    user = cur.fetchone()
    con.close()
    return user is not None
