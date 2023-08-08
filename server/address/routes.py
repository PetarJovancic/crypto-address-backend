from server import app
from server.models import User
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.address.controller import create_address, get_all_addresses, get_address


@app.route('/address', methods=['POST'])
@jwt_required()
def add_address() -> dict:
    '''
    create new address
    '''
    if request.is_json:
        data = request.get_json()

        result = create_address(data)


        new_address = {
            'id': result.public_id,
            'address': result.address
        }

        return {'message': new_address}, 201

@app.route('/address', methods=['GET'])
@jwt_required()
def list_addresses() -> dict:
    '''
    list of all addresses
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    addresses = get_all_addresses(page, per_page)
    result = [
        {
            'id': address.public_id,
            'address': address.address,
            'coin_name': address.coin_name,
            'account_id': address.account_id,
        } for address in addresses]

    return {'message': result}, 200

@app.route('/address/<id>', methods=['GET'])
@jwt_required()
def get_single_address(id):
    address = get_address(id)

    result = {
            'id': address.public_id,
            'address': address.address,
            'coin_name': address.coin_name,
            'account_id': address.account_id,
    }

    return {'message': result}, 200