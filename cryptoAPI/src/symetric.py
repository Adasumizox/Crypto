from crypto import Crypto
import base64
from cryptography.fernet import Fernet


class Symetric:

    def __init__(self):
        self.crypto = Crypto(key=self.generate_key())

    def set_key(self, key):
        self.crypto.key = key

    def set_text(self, text):
        self.crypto.text = text

    def set_ciphertext(self, ciphertext):
        self.crypto.ciphertext = ciphertext

    def get_text(self):
        return self.crypto.text

    def get_ciphertext(self):
        return self.crypto.ciphertext

    def generate_key(self) -> bytes:
        return Fernet.generate_key()

    def convert_key_to_string(self) -> bytes:
        return base64.b64decode(self.crypto.key)

    @staticmethod
    def convert_string_to_key(key) -> str:
        return base64.b64encode(key)

    # def encode_message(self) -> bool:
    # we need to think something out
