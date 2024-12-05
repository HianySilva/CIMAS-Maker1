from flask import Blueprint, request, jsonify
from entities.email_crud import add_email_domain_to_institution, list_email_domains_by_institution, is_email_domain_allowed, delete_email_domain

# Criando um Blueprint para as rotas de domínios de email
email_bp = Blueprint('email', __name__)

# Rota para adicionar um domínio de e-mail a uma instituição
@email_bp.route('/email-domain', methods=['POST'])
def add_domain():
    data = request.get_json()
    domain = data.get('domain')
    institution_id = data.get('institution_id')

    if not domain or not institution_id:
        return jsonify({"error": "Domínio e ID da instituição são obrigatórios!"}), 400

    message, status = add_email_domain_to_institution(domain, institution_id)
    return jsonify(message), status

# Rota para listar os domínios de e-mail de uma instituição
@email_bp.route('/email-domain/<int:institution_id>', methods=['GET'])
def list_domains(institution_id):
    domains, status = list_email_domains_by_institution(institution_id)
    return jsonify(domains), status

# Rota para verificar se o domínio de um e-mail é permitido
@email_bp.route('/email-domain/verify', methods=['POST'])
def verify_email_domain():
    data = request.get_json()
    email = data.get('email')
    institution_id = data.get('institution_id')

    if not email or not institution_id:
        return jsonify({"error": "E-mail e ID da instituição são obrigatórios!"}), 400

    is_allowed = is_email_domain_allowed(email, institution_id)
    if is_allowed:
        return jsonify({"message": "Domínio de e-mail permitido."}), 200
    else:
        return jsonify({"error": "Domínio de e-mail não permitido."}), 400

# Rota para deletar um domínio de e-mail
@email_bp.route('/email-domain/<int:domain_id>', methods=['DELETE'])
def delete_domain(domain_id):
    message = delete_email_domain(domain_id)
    return jsonify(message), 200
