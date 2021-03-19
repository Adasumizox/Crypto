import unittest
from hashing.src.HashHelper import HashHelper


class HashHelperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__hashHelper = HashHelper()

    def test_init(self):
        self.assertIsInstance(self.__hashHelper, HashHelper)

    def test_wrong_filepath(self):
        with self.assertRaises(FileNotFoundError):
            HashHelper.calculate_checksum("", "sha1")

    def test_wrong_algorithm(self):
        with self.assertRaises(AssertionError):
            HashHelper.calculate_checksum("./requirements.txt", "wrong")

    def tearDown(self) -> None:
        self.__hashHelper = None
