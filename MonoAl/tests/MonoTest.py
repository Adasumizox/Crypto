import unittest
from MonoAl.src.Mono import Mono


class MonoTest(unittest.TestCase):
    def setUp(self) -> None:
        self._mono = Mono("test")

    def test_init(self):
        self.assertIsInstance(self._mono, Mono)

    def test_is_english(self):
        self.assertTrue(self._mono.is_english("test"))

    def test_remove_whitespaces(self):
        self.assertEqual(self._mono.remove_whitespaces("test   whitespaces \t removal \n"), "testwhitespacesremoval")

    def test_transpose_columns(self):
        pass

    def test_transpose_rows(self):
        pass

    def test_cipher(self):
        pass

    def tearDown(self) -> None:
        self._mono = None
