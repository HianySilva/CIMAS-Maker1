import sqlite3
from sqlite3 import Error
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Função para criar um endereço
def create_address(street, number, city, state, postal_code):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO address (street, number, city, state, postal_code)
        VALUES (?, ?, ?, ?, ?)
    ''', (street, number, city, state, postal_code))
    
    conn.commit()
    conn.close()

# Função para obter um endereço por ID
def get_address_by_id(address_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM address WHERE id = ?
    ''', (address_id,))
    address = cursor.fetchone()
    
    conn.close()
    return address

# Função para listar todos os endereços
def get_all_addresses():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM address
    ''')
    addresses = cursor.fetchall()
    
    conn.close()
    return addresses

# Função para atualizar um endereço
def update_address(address_id, street=None, number=None, city=None, state=None, postal_code=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Prepara a lista de colunas para atualizar dinamicamente
    updates = []
    params = []
    
    if street:
        updates.append('street = ?')
        params.append(street)
    if number:
        updates.append('number = ?')
        params.append(number)
    if city:
        updates.append('city = ?')
        params.append(city)
    if state:
        updates.append('state = ?')
        params.append(state)
    if postal_code:
        updates.append('postal_code = ?')
        params.append(postal_code)
    
    params.append(address_id)
    
    cursor.execute(f'''
        UPDATE address SET {", ".join(updates)} WHERE id = ?
    ''', tuple(params))
    
    conn.commit()
    conn.close()

# Função para remover um endereço
def delete_address(address_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM address WHERE id = ?
    ''', (address_id,))
    
    conn.commit()
    conn.close()
