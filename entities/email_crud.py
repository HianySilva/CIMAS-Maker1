import sqlite3
import os

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config/database.db')

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DATABASE)

# Função para adicionar um domínio de e-mail para uma instituição
def add_email_domain_to_institution(domain, institution_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Verifica se o domínio já está registrado para essa instituição
        cursor.execute('''
            SELECT id FROM institution_email_domain
            WHERE domain = ? AND institution_id = ?
        ''', (domain, institution_id))

        existing_domain = cursor.fetchone()

        if existing_domain:
            return {"error": "Este domínio já está associado a essa instituição!"}, 400

        # Caso o domínio não exista para a instituição, insere o novo domínio
        cursor.execute('''
            INSERT INTO institution_email_domain (domain, institution_id)
            VALUES (?, ?)
        ''', (domain, institution_id))
        conn.commit()

    except sqlite3.IntegrityError as e:
        return {"error": f"Erro ao inserir domínio: {str(e)}"}, 400
    finally:
        conn.close()

    return {"message": "Domínio de e-mail associado à instituição com sucesso!"}, 201


# Função para listar todos os domínios de uma instituição
def list_email_domains_by_institution(institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, domain 
        FROM institution_email_domain 
        WHERE institution_id = ?
    ''', (institution_id,))
    domains = cursor.fetchall()
    conn.close()
    return [{"id": domain[0], "domain": domain[1]} for domain in domains], 200

# Função para verificar se um domínio de e-mail é permitido
def is_email_domain_allowed(email, institution_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Extrai o domínio do e-mail
    domain = email.split('@')[-1]
    
    # Busca na tabela de domínios permitidos para a instituição específica
    cursor.execute('''
        SELECT domain 
        FROM institution_email_domain 
        WHERE institution_id = ?
    ''', (institution_id,))
    allowed_domains = cursor.fetchall()
    conn.close()

    # Verifica se o domínio ou um subdomínio é permitido
    for allowed_domain in allowed_domains:
        if domain.endswith(allowed_domain[0]):  # Verifica subdomínios
            return True
    return False

# Função para deletar um domínio de e-mail
def delete_email_domain(domain_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM institution_email_domain WHERE id = ?', (domain_id,))
    conn.commit()
    conn.close()
    return {"message": "Domínio de e-mail removido com sucesso!"}
