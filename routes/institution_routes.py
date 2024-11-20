from flask import Blueprint, request, jsonify
from entities.institution_crud import create_institution, get_institution_by_id, get_all_institutions, update_institution, delete_institution
from entities.address_crud import create_address

# Criação do Blueprint para instituições
institution_bp = Blueprint('institution_bp', __name__)

# Rota para criar uma instituição
@institution_bp.route('/institution', methods=['POST'])
def create_new_institution():
    data = request.get_json()
    
    # Verifica se os campos necessários estão presentes
    name = data.get('name')
    cnpj = data.get('cnpj')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')  # Deverá ser um dict de endereço
    
    if not name or not cnpj or not phone or not email or not address:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400
    
    # Cria o endereço
    address_id = create_address(address['street'], address['number'], address['city'], address['state'], address['postal_code'])
    
    try:
        create_institution(name, cnpj, phone, email, address_id)
        return jsonify({"message": "Instituição criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter todas as instituições
@institution_bp.route('/institutions', methods=['GET'])
def list_institutions():
    try:
        institutions = get_all_institutions()
        return jsonify({"institutions": institutions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter uma instituição pelo ID
@institution_bp.route('/institution/<int:institution_id>', methods=['GET'])
def get_institution(institution_id):
    try:
        institution = get_institution_by_id(institution_id)
        if institution:
            return jsonify({"institution": institution}), 200
        else:
            return jsonify({"error": "Instituição não encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar uma instituição
@institution_bp.route('/institution/<int:institution_id>', methods=['PUT'])
def update_institution_data(institution_id):
    data = request.get_json()
    
    name = data.get('name')
    cnpj = data.get('cnpj')
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')  # Deverá ser um dict de endereço
    
    try:
        # Atualiza o endereço
        if address:
            address_id = create_address(address['street'], address['number'], address['city'], address['state'], address['postal_code'])
            data['address_id'] = address_id
        
        update_institution(institution_id, name, cnpj, phone, email, data.get('address_id'))
        return jsonify({"message": "Instituição atualizada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para deletar uma instituição
@institution_bp.route('/institution/<int:institution_id>', methods=['DELETE'])
def delete_institution_data(institution_id):
    try:
        delete_institution(institution_id)
        return jsonify({"message": "Instituição removida com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
