import hashlib
import secrets

from hashingPassword.src.DatabaseController import DatabaseController


class HashPasswordHelper:
    """Helper class for computing hashes for passwords"""
    SUPPORTED_PASSWORD_HASHING_ALGORITHMS = ["SHA512", "PBKDF2_HMAC"]

    @staticmethod
    def hash_password(password: str, salt: str, algorithm: str) -> str:
        """Hash provided password with salt
        :param password: user password
        :param salt: salt used
        :param algorithm: algorithm that we want to use
        :return hashed password"""
        assert algorithm in HashPasswordHelper.SUPPORTED_PASSWORD_HASHING_ALGORITHMS, "Algorithm not yet supported"
        if algorithm == 'SHA512':
            return hashlib.sha512(salt.encode("UTF-8") + password.encode("UTF-8")).hexdigest()
        elif algorithm == 'PBKDF2_HMAC':
            return hashlib.pbkdf2_hmac('sha512', str.encode(password), bytes.fromhex(salt), 100000)

    @staticmethod
    def generate_salt(nbytes: int = 16) -> str:
        """Generate salt with cryptographically strong random numbers
        :param nbytes: number of bytes default=16
        :return generated salt"""
        assert nbytes >= 1, "number of bytes must be more than 0"
        return secrets.token_hex(nbytes)

    @staticmethod
    def verify_password(database: str, username: str, password: str) -> bool:
        """Verify if password is the same as password in database

        :param database: database where we store hashes
        :param username: name of user
        :param password: password of user
        :return: result of comparison
        """
        db = DatabaseController(database)
        user_db_data = db.select_user_data(username)
        return user_db_data[0] == HashPasswordHelper.hash_password(password, user_db_data[1], user_db_data[2])
