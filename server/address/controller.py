from flask import abort
from server.models import User, Account, Address
from server import db
from sqlalchemy import exc
import uuid
from server.wallet.hd_wallet import Wallet


ALLOWED_SYMBOLS = ["BTC", "ETH", "QTUM", "LTC", "DOGE"]


def create_address(data):
    keys = list(data.keys())

    if 'cryptocurrency' not in keys or 'account_id' not in keys:
        abort(400, 'Invalid request')

    symbol = normalize_symbol(data['cryptocurrency'])
    if symbol not in ALLOWED_SYMBOLS:
        abort(400, f'Invalid request. Please select one of the following currencies ${ALLOWED_SYMBOLS}')
        
    account = Account.query.filter_by(id=data['account_id']).first()
    address = Address.query.filter_by(coin_name=symbol).first()

    if not account:
        abort(400, 'Account does not exist.')

    if address:
        abort(400, 'Address for this cryptocurreny already exists.')

    hd_wallet = Wallet()

    try:
        new_address = Address(
            public_id=str(uuid.uuid4()),
            account_id=account.id,
            coin_name=symbol,
            address=hd_wallet.generate_address_from_private_key(symbol, account),
        )

        db.session.add(new_address)
        db.session.commit()
    except exc.SQLAlchemyError:
        abort(500, 'Internal error.') 

    return new_address

def normalize_symbol(symbol: str) -> str:
    """Normalize entered symbol to existing format."""
    return symbol.upper()

def get_all_addresses(page, per_page):
    try:
        return Address.query.paginate(page=page, per_page=per_page, error_out=False)
    except Exception as e:
        abort(500, 'Internal server error')

def get_address(address_id):
    address = None

    try:
        address = db.session.query(Address).filter(
            Address.public_id == address_id).first()
    except exc.DataError:
        abort(400, 'Invalid name')
    except exc.SQLAlchemyError:
        abort(500, 'Internal server error')

    if not address:
        abort(404, 'Not Found')
    else:
        return address