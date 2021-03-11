import unittest
from cryptography.core.ROT import ROT


class TestROT(unittest.TestCase):

    def setUp(self) -> None:
        self.__ROT = ROT()

    def test_create_object_with_wrong_shift(self):
        with self.assertRaises(AssertionError):
            rot = ROT(-1)
        with self.assertRaises(TypeError):
            rot = ROT("ABC")

    def test_edge_shift(self):
        rot = ROT(0)
        self.assertEqual(rot.encrypt(text="crypto"), "crypto")
        rot = ROT(27)
        self.assertEqual(rot.encrypt(text="crypto"), "dszqup")

    def test_upper_case_cipher(self):
        self.assertEqual(self.__ROT.encrypt(text='CRYPTO'), 'Pelcgb')

    def test_upper_case_decipher(self):
        self.assertEqual(self.__ROT.decrypt(text='Pelcgb'), 'CRYPTO')

    def test_lower_case_cipher(self):
        self.assertEqual(self.__ROT.encrypt(text='crypto'), 'pELCGB')

    def test_lower_case_decipher(self):
        self.assertEqual(self.__ROT.decrypt(text='pELCGB'), 'crypto')

    def test_mixed_cipher(self):
        self.assertEqual(self.__ROT.encrypt(text='cryPTO'), 'pELcgb')

    def test_mixed_decipher(self):
        self.assertEqual(self.__ROT.decrypt(text='pELcgb'), 'cryPTO')

    def test_wrong_text(self):
        with self.assertRaises(AssertionError):
            self.__ROT.encrypt("")
        with self.assertRaises(AssertionError):
            self.__ROT.decrypt("")
        with self.assertRaises(TypeError):
            self.__ROT.encrypt(123)

    def test_number_punctation_cipher(self):
        self.assertEqual(self.__ROT.encrypt(text='Th1s Sh.ld n0t b# pr0b-em'), 'gu1F fu.yq A0G o# CE0o-rz')

    def tearDown(self) -> None:
        self.__ROT = None


if __name__ == '__main__':
    unittest.main()
