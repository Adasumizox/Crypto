import string
import random
from typing import Optional
#from polyglot.detect import Detector


class Mono:

    def __init__(self, text: str):
        text = self.remove_whitespaces(text)

        #assert Detector(text).language == "English", "text must be in english"

        self._text = text

    @staticmethod
    def remove_whitespaces(text: str) -> str:
        """ Static method for removing whitespaces from text

        :param text: text
        :return: text without whitespaces
        """
        return ''.join(text.split())

    def transpose_column(self, col_num: int) -> None:
        """ Method for transposing text according to number of columns

        :param col_num: number of columns
        """
        assert col_num > 0, "number of columns cannot be negative or zero"
        assert col_num < len(self._text), "number of columns must be lower than length of text"

        output_text = ""

        for x in range(0, col_num):
            output_text += self._text[0+x::col_num]

        self._text = output_text

    def transpose_rows(self, row_num: int) -> None:
        """ Method for transposing text according to number of rows

        :param: row_num: number of rows
        """
        assert row_num > 0, "number of rows cannot be negative or zero"
        assert row_num < len(self._text), "number of columns must be lower than length of text"

    def cipher(self, replace_alphabet: Optional[str]) -> str:
        """ create monoalphabetic cipher

        :param replace_alphabet: alphabet that we want to use in our cipher
        :return: ciphered text
        """
        if replace_alphabet is None:
            replace_alphabet = ''.join(random.sample(string.ascii_letters, len(string.ascii_letters)))
        else:
            assert len(replace_alphabet) == len(string.ascii_letters), "string is to short please assign every " \
                                                                       "letter from lowercase a to uppercase Z " \
                                                                       "without spaces "
        transition_table = str.maketrans(string.ascii_letters, replace_alphabet)
        return self._text.translate(transition_table)
