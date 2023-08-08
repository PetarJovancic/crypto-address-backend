from flask import abort
from server.models import User, Account
from server import db
from sqlalchemy import exc
import uuid
from server.wallet.hd_wallet import Wallet


def create_account(data, current_user):
    keys = list(data.keys())

    if 'account_name' not in keys:
        abort(400, 'Invalid request')

    user = User.query.filter_by(username=current_user).first()
    account = Account.query.filter_by(account_name=data['account_name']).first()

    if account:
        abort(400, 'Account already exists.')
    
    hd_wallet = Wallet()

    try:
        new_account = Account(
            public_id=str(uuid.uuid4()),
            user_id=user.id,
            account_name=data['account_name'],
            mnemonic=hd_wallet.generate_mnemonic(),
            passphrase=hd_wallet.generate_passphrase(),
        )

        db.session.add(new_account)
        db.session.commit()
    except exc.SQLAlchemyError:
        abort(500, 'Internal error.') 

    return new_account

def get_all_accounts():
    return db.session.query(Account).all()
