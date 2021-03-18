import hashlib
import secrets
import pyargon2
import bcrypt


class User:
    AVAILABLE_HASHING_ALGORITHMS = ["Bcrypt", "Argon2", "PBKDF2"]

    def __init__(self, login: str, password: str, algorithm: str = "Argon2"):
        assert algorithm in self.AVAILABLE_HASHING_ALGORITHMS, "Algorithm not yet supported"
        self._algorithm = algorithm
        self._login = login,
        self._salt = self.generate_string_salt(16)
        self.password = hash(password)

    @staticmethod
    def generate_string_salt(nbytes: int = 16) -> bytes:
        return secrets.token_bytes(nbytes)

    def hash(self, password):
        if self._algorithm == "Argon2":
            return pyargon2.hash(password, str(self._salt))
        elif self._algorithm == "Bcrypt":
            return bcrypt.hashpw(str.encode(password), self._salt)
        elif self._algorithm == "PBKDF2":
            return hashlib.pbkdf2_hmac("sha256", str.encode(password), self._salt, 1000000)