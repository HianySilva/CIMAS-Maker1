import sqlite3
from sqlite3 import Error
from .address_crud import create_address, get_address_by_id
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Função para criar uma instituição
def create_institution(name, cnpj, phone, email, address_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO institution (name, cnpj, phone, email, address_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, cnpj, phone, email, address_id))
    
    conn.commit()
    conn.close()

# Função para obter uma instituição por ID
def get_institution_by_id(institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM institution WHERE id = ?
    ''', (institution_id,))
    institution = cursor.fetchone()
    
    conn.close()
    return institution

# Função para listar todas as instituições
def get_all_institutions():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM institution
    ''')
    institutions = cursor.fetchall()
    
    conn.close()
    return institutions

# Função para atualizar uma instituição
def update_institution(institution_id, name=None, cnpj=None, phone=None, email=None, address_id=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Prepara a lista de colunas para atualizar dinamicamente
    updates = []
    params = []
    
    if name:
        updates.append('name = ?')
        params.append(name)
    if cnpj:
        updates.append('cnpj = ?')
        params.append(cnpj)
    if phone:
        updates.append('phone = ?')
        params.append(phone)
    if email:
        updates.append('email = ?')
        params.append(email)
    if address_id:
        updates.append('address_id = ?')
        params.append(address_id)
    
    params.append(institution_id)
    
    cursor.execute(f'''
        UPDATE institution SET {", ".join(updates)} WHERE id = ?
    ''', tuple(params))
    
    conn.commit()
    conn.close()

# Função para remover uma instituição
def delete_institution(institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM institution WHERE id = ?
    ''', (institution_id,))
    
    conn.commit()
    conn.close()
