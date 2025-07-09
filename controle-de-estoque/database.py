# controle-de-estoque/database.py

import sqlite3
import hashlib

def hash_password(password):
    """Criptografa a senha usando SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def setup_database():
    """
    Cria as tabelas do banco de dados e insere um usuário administrador padrão.
    """
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Criar tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        profile TEXT NOT NULL
    )
    ''')

    # Criar tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL,
        min_quantity INTEGER NOT NULL
    )
    ''')

    # Verificar se o usuário admin já existe
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone() is None:
        # Senha padrão para o admin é 'admin'
        admin_password_hash = hash_password('admin')
        cursor.execute('''
        INSERT INTO users (username, password_hash, profile)
        VALUES (?, ?, ?)
        ''', ('admin', admin_password_hash, 'Administrador'))
        print("Usuário 'admin' criado com a senha 'admin'.")
    else:
        print("Usuário 'admin' já existe.")

    conn.commit()
    conn.close()
    print("Banco de dados 'inventory.db' configurado com sucesso.")

if __name__ == '__main__':
    setup_database()