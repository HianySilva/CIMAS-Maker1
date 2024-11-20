from flask import Blueprint, request, jsonify
from entities.address_crud import create_address, get_address_by_id, get_all_addresses, update_address, delete_address

# Criação do Blueprint para endereços
address_bp = Blueprint('address_bp', __name__)

# Rota para criar um endereço
@address_bp.route('/address', methods=['POST'])
def create_new_address():
    data = request.get_json()
    
    # Verifica se os campos necessários estão presentes
    street = data.get('street')
    number = data.get('number')
    city = data.get('city')
    state = data.get('state')
    postal_code = data.get('postal_code')

    if not street or not number or not city or not state or not postal_code:
        return jsonify({"error": "Todos os campos são obrigatórios"}), 400

    try:
        create_address(street, number, city, state, postal_code)
        return jsonify({"message": "Endereço criado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter todos os endereços
@address_bp.route('/addresses', methods=['GET'])
def list_addresses():
    try:
        addresses = get_all_addresses()
        return jsonify({"addresses": addresses}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para obter um endereço pelo ID
@address_bp.route('/address/<int:address_id>', methods=['GET'])
def get_address(address_id):
    try:
        address = get_address_by_id(address_id)
        if address:
            return jsonify({"address": address}), 200
        else:
            return jsonify({"error": "Endereço não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar um endereço
@address_bp.route('/address/<int:address_id>', methods=['PUT'])
def update_address_data(address_id):
    data = request.get_json()
    
    street = data.get('street')
    number = data.get('number')
    city = data.get('city')
    state = data.get('state')
    postal_code = data.get('postal_code')

    try:
        update_address(address_id, street, number, city, state, postal_code)
        return jsonify({"message": "Endereço atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para deletar um endereço
@address_bp.route('/address/<int:address_id>', methods=['DELETE'])
def delete_address_data(address_id):
    try:
        delete_address(address_id)
        return jsonify({"message": "Endereço removido com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
