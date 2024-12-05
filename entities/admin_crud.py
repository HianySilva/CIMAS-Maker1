import sqlite3
import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash 

# Criação da instância Flask
app = Flask(__name__)

# Configuração do banco de dados
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Função para criar um administrador
def create_admin(data):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Criptografar a senha
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)

        # Inserir no banco de dados
        cursor.execute('''
            INSERT INTO admin (email, username, password)
            VALUES (?, ?, ?)
        ''', (data['email'], data['name'], hashed_password))

        conn.commit()
        success_message = "Administrador criado com sucesso!"
        return {"message": success_message}
    
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            error_message = "Email já existe!"
            return {"error": error_message}
        if "username" in str(e):
            error_message = "Username já existe!"
            return {"error": error_message}
    finally:
        conn.close()


# Função para listar os administradores
def get_all_admins():
    try:
        conn = connect_db()  # Conectando ao banco de dados
        cursor = conn.cursor()
        
        # Modificando a consulta para também retornar a senha
        cursor.execute('SELECT id, email, username, password FROM admin')  # Consulta SQL incluindo a senha
        admins = cursor.fetchall()  # Recupera todos os resultados da consulta
        conn.close()  # Fecha a conexão com o banco de dados

        # Retorna os dados no formato que será consumido pelo frontend, incluindo a senha
        return [{"id": admin[0], "email": admin[1], "username": admin[2], "password": admin[3]} for admin in admins]
    
    except Exception as e:
        # Em caso de erro, retorna um erro com a mensagem
        print(f"Erro ao buscar administradores: {e}")
        return []  # Retorna uma lista vazia se houver erro


# Função para atualizar um administrador
def update_admin(id, data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE admin 
        SET email = ?, username = ?, password = ? 
        WHERE id = ?
    ''', (data['email'], data['username'], data['password'], id))
    conn.commit()
    conn.close()
    return {"message": "Administrador atualizado com sucesso!"}

# Função para deletar um administrador
def delete_admin(id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Verificar se o administrador existe antes de excluir
    cursor.execute('SELECT * FROM admin WHERE id = ?', (id,))
    admin = cursor.fetchone()
    
    if not admin:
        conn.close()
        return {"message": "Administrador não encontrado"}, 404
    
    # Exclui o administrador
    cursor.execute('DELETE FROM admin WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return {"message": "Administrador deletado com sucesso!"}, 200


def get_admin_by_email_and_password(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Consulta para buscar o administrador pelo email
    cursor.execute('''SELECT id, username, email, password FROM admin WHERE email = ?''', (email,))
    admin = cursor.fetchone()  # Retorna o primeiro administrador encontrado
    
    conn.close()
    
    if admin:
        # Verifica se a senha fornecida bate com a senha criptografada
        if check_password_hash(admin[3], password):  # admin[3] é a senha criptografada
            return {"id": admin[0], "username": admin[1], "email": admin[2]}  # Retorna os dados do administrador
    return None  # Retorna None se não encontrar ou se a senha não bater
