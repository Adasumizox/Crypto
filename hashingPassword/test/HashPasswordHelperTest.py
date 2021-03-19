import unittest
from hashingPassword.src.HashPasswordHelper import  HashPasswordHelper


class HashHelperTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__hashPasswordHelper = HashPasswordHelper()

    def test_init(self):
        self.assertIsInstance(self.__hashPasswordHelper, HashPasswordHelper)

    def test_wrong_password_algorithm(self):
        with self.assertRaises(AssertionError):
            HashPasswordHelper.hash_password("test", "test2", "bcrypt")

    def test_negative_nbytes_salt(self):
        with self.assertRaises(AssertionError):
            HashPasswordHelper.generate_salt(-5)

    def test_password_hash(self):
        self.assertEqual(HashPasswordHelper.hash_password("test", "test", "SHA512"),
                         "125d6d03b32c84d492747f79cf0bf6e179d287f341384eb5d6d3197525ad6be8" +
                         "e6df0116032935698f99a09e265073d1d6c32c274591bf1d0a20ad67cba921bc")

    def tearDown(self) -> None:
        self.__hashHelper = None

