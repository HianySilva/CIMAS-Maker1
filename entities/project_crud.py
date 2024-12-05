import sqlite3
import os
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)


def insert_project(title, description, file_path, image_path):
    """
    Insere um novo projeto no banco de dados.
    """
    query = """
    INSERT INTO projects (title, description, file_path, image_path)
    VALUES (?, ?, ?, ?)
    """
    conn = connect_db()
    conn.execute(query, (title, description, file_path, image_path))
    conn.commit()

def get_all_projects():
    """
    Recupera todos os projetos do banco de dados.
    """
    query = "SELECT * FROM projects"
    conn = connect_db()
    return conn.execute(query).fetchall()

    
def update_project(project_id, title, description, file_path=None, image_path=None):
    """
    Atualiza um projeto no banco de dados.
    """
    query = """
    UPDATE projects
    SET title = ?, description = ?, file_path = COALESCE(?, file_path), image_path = COALESCE(?, image_path)
    WHERE id = ?
    """
    conn = connect_db()
    conn.execute(query, (title, description, file_path, image_path, project_id))
    conn.commit()


def delete_project(project_id):
    """
    Remove um projeto do banco de dados.
    """
    query = "DELETE FROM projects WHERE id = ?"
    conn = connect_db()
    conn.execute(query, (project_id,))
    conn.commit()


def get_project_by_id(project_id):
    """
    Recupera um único projeto pelo ID.
    """
    query = "SELECT * FROM projects WHERE id = ?"
    conn = connect_db()
    return conn.execute(query, (project_id,)).fetchone()