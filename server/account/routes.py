from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from server import app
from server.models import Account
from server.account.controller import create_account, get_all_accounts


@app.route('/account', methods=['POST'])
@jwt_required()
def add_account() -> dict:
    '''
    create new account
    '''
    if request.is_json:
        data = request.get_json()

        current_user = get_jwt_identity()
        result = create_account(data, current_user)


        new_account = {
            'id': result.id,
            'account_name': result.account_name
        }

        return {'message': new_account}, 201

@app.route('/account', methods=['GET'])
@jwt_required()
def list_accounts() -> dict:
    '''
    list of all accounts
    '''
    accounts = get_all_accounts()
    result = [
        {
            'id': account.id,
            'account_name': account.account_name,
            'user_id': account.user_id,
        } for account in accounts]

    return {'message': result}, 201