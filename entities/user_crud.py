import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Função para criar um usuário(Registro)
def create_user(data):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user (name, dateofbirth, email, password, institutionName) 
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['dateofbirth'], data['email'], data['password'], data['institutionName']))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            return {"error": "Email já existe!"}, 400
    finally:
        conn.close()
    return {"message": "Usuário criado com sucesso!"}, 201

# Função para listar todos os usuários
def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, institutionName FROM user')
    users = cursor.fetchall()
    conn.close()
    return [
        {"id": user[0], "name": user[1], "email": user[2], "institutionName": user[3]} 
        for user in users
    ], 200

#Função para achar um usuario pelo email e senha(Login)
def get_user_by_email_and_password(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT id, name, email FROM user WHERE email = ? AND password = ?''', (email, password))
    user = cursor.fetchone()  # Busca o primeiro usuário que corresponda
    
    conn.close()
    
    if user:
        return {"id": user[0], "name": user[1], "email": user[2]}  # Retorna o usuário se encontrado
    return None  # Retorna None caso não encontre


#Função para achar um usuario pelo id(Login e seção)
def get_user_by_id(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''SELECT id, name FROM user WHERE id = ?''', (user_id,))
    user = cursor.fetchone()  # Retorna o primeiro usuário com o id correspondente
    
    conn.close()
    
    if user:
        return {"id": user[0], "name": user[1]}  # Retorna o usuário
    return None  # Retorna None caso não encontre

# Função para atualizar um usuário
def update_user(id, data):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user 
        SET name = ?, dateofbirth = ?, email = ?, password = ?, institutionName = ? 
        WHERE id = ?
    ''', (data['name'], data['dateofbirth'], data['email'], data['password'], data['institutionName'], id))
    conn.commit()
    conn.close()
    return {"message": "Usuário atualizado com sucesso!"}

# Função para deletar um usuário
def delete_user(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {"message": "Usuário deletado com sucesso!"}
