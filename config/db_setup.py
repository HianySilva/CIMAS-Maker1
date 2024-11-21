import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Criando as Tabelas
def init_db():
    # Antes de tudo, exclua o banco de dados se ele já existir
    #if os.path.exists(DATABASE):
      #  os.remove(DATABASE)
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

    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dateofbirth TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        institution_id INTEGER NOT NULL,  -- FK para instituição
        FOREIGN KEY (institution_id) REFERENCES institution(id) ON DELETE CASCADE
    )
''')

# Tabela de instituições
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS institution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cnpj TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        address_id INTEGER,  -- FK para endereços
        FOREIGN KEY (address_id) REFERENCES address(id)
    )
''')

    # Tabela de address (Endereços das instituições)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS address (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT NOT NULL,            -- Rua
            number TEXT NOT NULL,            -- Número
            city TEXT NOT NULL,              -- Cidade
            state TEXT NOT NULL,             -- Estado
            postal_code TEXT NOT NULL        -- CEP
        )
    ''')
    # Tabela para domínios de email das instituições
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS institution_email_domain (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT NOT NULL UNIQUE,  -- Ex.: "@empresa.com"
        institution_id INTEGER NOT NULL,  -- FK para instituição
        FOREIGN KEY (institution_id) REFERENCES institution(id) ON DELETE CASCADE
    )
''')


    # Commit para garantir que as tabelas sejam criadas
    conn.commit()

    # Verifica as tabelas criadas
    #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #tables = cursor.fetchall()
    #print("Tabelas no banco de dados:", tables)


    conn.close()

# Chama a função init_db para criar as tabelas
print("Iniciando a criação do banco de dados...")
init_db()



