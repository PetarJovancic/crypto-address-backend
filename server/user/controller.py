from server import db
from server.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy import exc
from flask_jwt_extended import create_access_token
from flask import abort


def register_user(data):
    keys = list(data.keys())

    if 'username' not in keys or 'password' not in keys:
        abort(400, 'Invalid request')

    user = User.query.filter_by(username=data['username']).first()

    if user:
        abort(400, 'User already exists.')

    if '@' not in data["email"] or '.' not in data["email"]:
        abort(401, 'Invalid email.')
    
    hashed_password = generate_password_hash(data["password"],
    method='sha256')

    try:
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(hashed_password)

        db.session.add(new_user)
        db.session.commit()
    except exc.SQLAlchemyError:
        abort(500, 'Internal error.') 

    return new_user

def login(data):
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        abort(401, 'User does not exist.') 

    if check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
    
        return access_token
    else:
        abort(403, 'Wrong password.') 