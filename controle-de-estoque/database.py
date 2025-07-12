# controle-de-estoque/database.py


import sqlite3
import hashlib

DB_NAME = 'inventory.db'

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def connect_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Cria as tabelas de usuários e produtos se não existirem."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            profile TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            min_quantity INTEGER NOT NULL
        )
    ''')

    # Cria um usuário admin padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password_hash, profile) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "Administrador")
        )

    conn.commit()
    conn.close()
