from server import app
from server.models import User
from flask import request
from server.user.controller import register_user, login


@app.route('/user/register', methods=['POST'])
def add_user() -> dict:
    '''
    add new user
    '''
    if request.is_json:
        data = request.get_json()
        result = register_user(data)


        new_user = {
            'id': result.public_id,
            'email': result.email,
            'username': result.username
        }

        return {'message': new_user}, 201

@app.route("/user/login", methods=["POST"])
def user_login() -> dict:
    '''
    get jwt access token when user is logged in
    '''
    data = request.get_json()
    result = login(data)
    
    return {'message': {'access_token': result, 
                             "token_type": "bearer"}}, 200