import sqlite3
import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash

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

    # Hash da senha
    hashed_password = generate_password_hash(data['password'])

    try:
        cursor.execute('''INSERT INTO admin (email, username, password) VALUES (?, ?, ?)''', 
                       (data['email'], data['name'], hashed_password))
        conn.commit()
        success_message = "Administrador criado com sucesso!"
        return success_message
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            error_message = "Email já existe!"
            return error_message
        if "username" in str(e):
            error_message = "Username já existe!"
            return error_message
    finally:
        conn.close()

# Função para criar administrador via rota
@app.route('/admin', methods=['POST'])
def create_admin_route():
    data = request.form.to_dict()
    message = create_admin(data)
    
    # Verifica se a mensagem é de sucesso ou erro
    if 'Administrador criado com sucesso!' in message:
        return render_template('admin_dashboard.html', success_message=message)
    else:
        return render_template('admin_dashboard.html', error_message=message)


# Função para listar os administradores
def get_all_admins():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, username FROM admin')
    admins = cursor.fetchall()
    conn.close()
    return [
        {"id": admin[0], "email": admin[1], "username": admin[2]} 
        for admin in admins
    ], 200

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
    cursor.execute('DELETE FROM admin WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {"message": "Administrador deletado com sucesso!"}


def get_admin_by_email_and_password(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT id, username, email FROM admin WHERE email = ? AND password = ?''', (email, password))
    admin = cursor.fetchone()  # Retorna o primeiro administrador encontrado
    
    conn.close()
    
    if admin:
        return {"id": admin[0], "username": admin[1], "email": admin[2]}  # Retorna o admin se encontrado
    return None  # Retorna None se não encontrar
