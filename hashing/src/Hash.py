import hashlib
import timeit
import secrets

from hashing.src.DatabaseController import DatabaseController

class HashHelper:
    """Helper class for computing hashes"""

    SUPPORTED_PASSWORD_HASHING_ALGORITHMS = ["SHA512", "PBKDF2_HMAC"]

    def __init__(self):
        """Constructor for Hash"""
        pass

    @staticmethod
    def hashing_time_for_all_algorithms(text: str, loops: int = 1000000) -> list:
        """Method that measure time of all hashing algorithm.
           Number of loops affects accuracy and speed.

        :param text: input that will be hashed
        :param loops: number of loops that will be executed to measure time default = 1000000
        :returns: list that contains name of algorithm and time of hashing provided text
        """
        outputs = []
        for algorithm in hashlib.algorithms_available:
            hash = hashlib.new(algorithm)
            if algorithm in ('shake_128', 'shake_256'):
                outputs.append(
                    [algorithm, timeit.timeit(lambda: hash.update(text.encode("UTF-8")), number=loops),
                     hash.hexdigest(length=64)])
            else:
                outputs.append(
                    [algorithm, timeit.timeit(lambda: hash.update(text.encode("UTF-8")), number=loops),
                     hash.hexdigest()])
        return outputs

    @staticmethod
    def calculate_checksum(filepath: str, algorithm: str, chunk_num_blocks=128) -> str:
        """Calculate checksum of file

        :param filepath: path to the file
        :param algorithm: hashing algorithm
        :param chunk_num_blocks: number of chunks that we want to divide file
        :return: hash of file
        """
        assert (algorithm in hashlib.algorithms_available), "Algorithm not supported"

        hashed = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_num_blocks * hashed.block_size):
                hashed.update(chunk)

            return hashed.hexdigest()

    @staticmethod
    def compare_file_with_checksum(filepath: str, checksum: str, algorithm: str) -> bool:
        """Compare checksum of file with hash

        :param filepath: path to the file
        :param checksum: checksum that we compare our file with
        :param algorithm: hashing algorithm that we choose
        :return: result of comparison
        """

        assert (algorithm in hashlib.algorithms_available), "Algorithm not supported"

        file_checksum = HashHelper.calculate_checksum(filepath, algorithm)

        return file_checksum == checksum

    @staticmethod
    def generate_hash_size_times(length: int, algorithm: str, step: int = 1, loops: int = 1000000) -> list:
        """Generate array of execution time of algorithm dependent on data length.
           Data is generated from length 1 to provided length

        :param length: size of input that we would like to generate
        :param algorithm: hashing algorithm that we choose
        :param step: break between size of text default = 1
        :param loops: number of loops that will be executed to measure time default = 1000000
        :returns: list that contains execution times of algorithm with data """
        assert (algorithm in hashlib.algorithms_available), "Algorithm not supported"
        outputs = []
        for i in range(0, length, step):
            text = 'a' * i
            outputs.append(timeit.timeit(lambda: hashlib.new('sha1', text.encode('UTF-8')), number=loops))
        return outputs

    @staticmethod
    def display_plot(data: list) -> None:
        """Generate plot line plot from provided data
        :param data: data that we want to visualize on plot"""
        import plotly.express as px
        fig = px.line(data)
        fig.show()

    @staticmethod
    def hash_password(password: str, salt: str, algorithm: str) -> str:
        """Hash provided password with salt
        :param password: user password
        :param salt: salt used
        :param algorithm: algorithm that we want to use
        :return hashed password"""
        assert algorithm in HashHelper.SUPPORTED_PASSWORD_HASHING_ALGORITHMS, "Algorithm not yet supported"
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
        db = DatabaseController(database)
        user_db_data = db.select_user_data(username)
        return user_db_data[0] == HashHelper.hash_password(password, user_db_data[1], user_db_data[2])