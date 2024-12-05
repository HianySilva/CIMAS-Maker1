from flask import Blueprint, request, jsonify
from entities.admin_crud import create_admin, get_all_admins, update_admin, delete_admin

# Criando o Blueprint
admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/test')
def test_route():
    return "Acesso à rota de teste bem-sucedido!"

# Rota para criar um administrador
@admin_bp.route('/admin', methods=['POST'])
def create_admin_route():
    data = request.get_json()  # Recebe os dados JSON enviados na requisição
    return create_admin(data)

# Rota para listar todos os administradores
@admin_bp.route('/admin', methods=['GET'])
def get_all_admins_route():
    return jsonify(get_all_admins())

# Rota para atualizar um administrador
@admin_bp.route('/admin/<int:id>', methods=['PUT'])
def update_admin_route(id):
    data = request.get_json()
    return update_admin(id, data)

# Rota para deletar um administrador
@admin_bp.route('/admin/<int:id>', methods=['DELETE'])
def delete_admin_route(id):
    return delete_admin(id)
