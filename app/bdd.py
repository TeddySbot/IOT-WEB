import sqlite3
import hashlib

DB_PATH = "pots.db"

# ---------- Connexion DB ---------- #
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Init DB ---------- #
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS pots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            topic TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# ---------- Hash mot de passe ---------- #
def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- CRUD UTILISATEURS ---------- #
def create_user(username, password):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_pwd(password))
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_user(username, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_pwd(password))
    ).fetchone()
    return user
