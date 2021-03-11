from hunspell import Hunspell
import string


class ROT:
    ALPHABET_LETTER_COUNT = 26
    ALPHABET = alphabet = string.ascii_letters

    def __init__(self, shift: int = 13):
        # shift cannot be negative
        assert shift >= 0

        self._shift = shift % self.ALPHABET_LETTER_COUNT

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, new_shift):
        if new_shift < 0:
            raise ValueError
        self._shift = new_shift

    def __make_shift_transitions(self, is_plaintext: bool = True) -> dict:
        """ Creating transition table for each letter of alphabet according to shift

        :param is_plaintext: flag that decide if text is already encrypted or not
        :return: dictionary of transitions
        """
        shifted_alphabet = self.ALPHABET[self._shift:] + self.ALPHABET[:self._shift]
        if is_plaintext:
            return str.maketrans(self.ALPHABET, shifted_alphabet)
        return str.maketrans(shifted_alphabet, self.ALPHABET)

    def encrypt(self, text: str) -> str:
        """ Encryption of source text according to provided shift

        :param text: content that we want to encrypt
        :return: encrypted string
        """
        assert len(text) > 0

        return text.translate(self.__make_shift_transitions())

    def decrypt(self, text: str) -> str:
        """ Decryption of source text according to provided shift

        :param text: encrypted string that we want to decrypt
        :return: decrypted string
        """
        assert len(text) > 0

        return text.translate(self.__make_shift_transitions(is_plaintext=False))

    # def manualBruteforce(text):
    #
    #     rotations = []
    #
    #     for i in range(1, 26):
    #         rotations.append(text.translate(makeShiftTransitions(i)))
    #
    #     return rotations
    #
    #
    # def showRotations(arrays):
    #     for i, rotation in enumerate(arrays, 1):
    #         print("ROT {}: {}".format(i, rotation))
    #
    #
    # def automaticSolve(text):
    #     h = Hunspell()
    #     rotations = manualBruteforce(text)
    #     for i, rotation in enumerate(rotations, 1):
    #         if h.spell(rotation):
    #             print("ROT {}: {}".format(i, rotation))
