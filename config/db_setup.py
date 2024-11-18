import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Criando as Tabelas
def init_db():
    # Antes de tudo, exclua o banco de dados se ele já existir
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    
    # Agora, criamos o banco de dados e as tabelas corretamente
    conn = connect_db()
    cursor = conn.cursor()
    
    # Tabela de admin
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Tabela de user
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dateofbirth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            institutionName TEXT NOT NULL
        )
    ''')

    # Commit para garantir que as tabelas sejam criadas
    conn.commit()
    conn.close()

# Chama a função init_db para criar as tabelas
init_db()



