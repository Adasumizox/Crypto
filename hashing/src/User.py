import secrets
import bcrypt
from pyargon2 import hash


class User:
    AVAILABLE_HASHING_ALGORITHMS = ["SHA1", "Bcrypt", "Argon2", "PBKDF2"]

    def __init__(self, login: str, password: str, algorithm: str = "Argon2"):
        assert algorithm in self.AVAILABLE_HASHING_ALGORITHMS, "Algorithm not yet supported"
        self._algorithm = algorithm
        self._login = login,
        self._salt = None
        self._password = None
