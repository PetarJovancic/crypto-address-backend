import base64

from Crypto.Cipher import AES
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Util.Padding import pad, unpad
from server.utils.keys_loader import KeysLoader


class Encoder:
    """AES encoder."""

    def __init__(self, key_parts):
        self._bs = AES.block_size
        key_parts = [
            (idx, base64.b64decode(key_part.encode()))
            for idx, key_part in key_parts
        ]
        self._key = Shamir.combine(key_parts, ssss=False)

    @classmethod
    def get_encoder(cls):
        """Get Encoder class and context."""
        return cls(KeysLoader.get_keys_loader().load_aes_keys())

    def encrypt(self, raw):
        """Encrypt incoming string."""
        raw = pad(raw.encode(), self._bs)
        cipher = AES.new(key=self._key, mode=AES.MODE_EAX)
        encrypted, tag, nonce = (
            cipher.encrypt(raw),
            cipher.digest(),
            cipher.nonce,
        )
        return base64.b64encode(nonce + tag + encrypted).decode("utf-8")

    def decrypt(self, enc):
        """Decrypt incoming string."""
        enc = base64.b64decode(enc)
        nonce, tag, encrypted = (
            enc[: self._bs],
            enc[self._bs : 2 * self._bs],
            enc[2 * self._bs :],
        )
        cipher = AES.new(key=self._key, mode=AES.MODE_EAX, nonce=nonce)
        raw = cipher.decrypt(encrypted)
        cipher.verify(tag)
        return unpad(raw, self._bs).decode("utf-8")