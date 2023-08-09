from hdwallet import HDWallet
from hdwallet.utils import generate_mnemonic, generate_passphrase
from server.utils.encoder import Encoder
from server import Config
from dotenv import load_dotenv


class Wallet:
    def __init__(self):
        load_dotenv()
        self.encoder = Encoder.get_encoder()
        self.language = Config.WALLET_LANGUAGE
        self.strength = Config.WALLET_STRENGTH
        self.passphrase_lenght = Config.PASSPHRASE_LENGHT

    def generate_mnemonic(self):
        """Generate account mnemonic phrase."""
        mnemonic = generate_mnemonic(
            language=self.language, strength=int(self.strength))
        return self.encoder.encrypt(mnemonic)

    def generate_passphrase(self):
        """Generate account passphrase"""
        passphrase = generate_passphrase(length=int(self.passphrase_lenght))
        return self.encoder.encrypt(passphrase)

    def generate_private_key(self, symbol, account):
        """Generate private key"""
        _hd_wallet = self._get_wallet(symbol, account)
        return _hd_wallet.private_key()

    def generate_address_from_private_key(self, symbol, account):
        """Generate address for an account."""
        _private_key = self.generate_private_key(symbol, account)
        hd_wallet = HDWallet(symbol=symbol)
        hd_wallet.from_private_key(private_key=_private_key)
        return hd_wallet.p2pkh_address()
        
    def _get_wallet(self, symbol, account):
        """Retrieve wallet for an account."""
        _hd_wallet = HDWallet(symbol=symbol, use_default_path=True)
        _hd_wallet.from_mnemonic(
            mnemonic=self.encoder.decrypt(account.mnemonic),
            language=self.language,
            passphrase=self.encoder.decrypt(account.passphrase),
        )

        return _hd_wallet

