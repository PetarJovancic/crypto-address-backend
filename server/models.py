from server import db
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))
    email = db.Column(db.String(50))

    accounts = db.relationship('Account', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = password


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    account_name = db.Column(db.String(50))
    mnemonic = db.Column(db.String(200))
    passphrase = db.Column(db.String(200))

    addresses = db.relationship('Address', backref='account', lazy=True)
    
    def __repr__(self):
        return f'<Account {self.account_name}>'
    

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key = True)
    
    public_id = db.Column(db.String(50), unique = True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
        nullable=False)

    address = db.Column(db.String(200))
    coin_name = db.Column(db.String(50))

    def __repr__(self):
        return f'<Address {self.coin_name}>'