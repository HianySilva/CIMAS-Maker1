from flask import Blueprint, request, jsonify, render_template
from entities.admin_crud import create_admin, get_all_admins, update_admin, delete_admin

# Criando o Blueprint
admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/test')
def test_route():
    return "Acesso à rota de teste bem-sucedido!"

# Rota para criar um administrador
@admin_bp.route('/admin', methods=['POST'])
def create_admin_route():
    if request.is_json:  # Se os dados forem enviados no formato JSON
        data = request.get_json()
    else:  # Se os dados forem enviados por um formulário HTML
        data = request.form.to_dict()
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

@admin_bp.route('/admin', methods=['GET'])
def admin_dashboard():
    admins = get_all_admins()  # Função que busca todos os administradores no banco de dados
    user = {"name": "Admin Master"}  # Simulação de um usuário autenticado
    return render_template('admin_dashboard.html', user=user, admins=admins)

# Rota para deletar um administrador
@admin_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin_route(admin_id):
    from entities.admin_crud import delete_admin  # Importe a lógica de exclusão
    result = delete_admin(admin_id)
    if result:
        return jsonify({"message": "Administrador excluído com sucesso"}), 200
    return jsonify({"message": "Erro ao excluir administrador"}), 400
