import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"


class User:

    def __init__(self, row):
        self.id = row["id"]
        self.username = row["username"]
        self.email = row["email"]

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, email, password):
    conn = get_db()

    hashed_password = generate_password_hash(password)

    conn.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password)
    )

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    return user


def check_password(user, password):
    return check_password_hash(user["password"], password)