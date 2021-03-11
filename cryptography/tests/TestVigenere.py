import unittest
from cryptography.core.Vigenere import Vigenere


class TestVigenere(unittest.TestCase):

    def setUp(self) -> None:
        self.__Vigenere = Vigenere('vigenere')

    def test_cipher(self):
        self.assertEqual(self.__Vigenere.cipher('cryptography'), 'XZETGSXVVXNC')
        self.assertEqual(self.__Vigenere.cipher('CRYPTOGRAPHY'), 'XZETGSXVVXNC')
        #self.__Vigenere.key('VIGENERE')
        #self.assertEqual(self.__Vigenere.cipher('cryptography'), 'XZETGSXVVXNC')
        #self.assertEqual(self.__Vigenere('CRYPTOGRAPHY'), 'XZETGSXVVXNC')
        #self.__Vigenere.key('vigenere')

    def test_decipher(self):
        self.assertEqual(self.__Vigenere.decipher('xzetgsxvvxnc'), 'CRYPTOGRAPHY')
        self.assertEqual(self.__Vigenere.decipher('XZETGSXVVXNC'), 'CRYPTOGRAPHY')
        #self.__Vigenere.key('VIGENERE')
        #self.assertEqual(self.__Vigenere.decipher('xzetgsxvvxnc'), 'CRYPTOGRAPHY')
        #self.assertEqual(self.__Vigenere.decipher('XZETGSXVVXNC'), 'CRYPTOGRAPHY')
        #self.__Vigenere.key('vigenere')

    def test_number_punctation_cipher(self):
        self.assertEqual(self.__Vigenere.decipher('XZETGSXVVXNC..-'), 'CRYPTOGRAPHY..-')
        self.assertEqual(self.__Vigenere.cipher('CRYPTOGRAPHY..-'), 'XZETGSXVVXNC..-')

    def tearDown(self) -> None:
        self.__Vigenere = None


if __name__ == '__main__':
    unittest.main()
