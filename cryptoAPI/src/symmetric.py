from crypto import Crypto
from typing import Union
import base64
from cryptography.fernet import Fernet


class Symmetric:
    @staticmethod
    def generate_key() -> bytes:
        """

        :return:
        """
        return Fernet.generate_key()

    @staticmethod
    def convert_to_base64_hex(s: Union[bytes,str]) -> bytes:
        return base64.urlsafe_b64decode(s).hex()

