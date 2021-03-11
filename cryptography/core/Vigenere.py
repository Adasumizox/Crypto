import math


class Vigenere:

    def __init__(self, key: str):
        assert len(key) > 0

        self._key = key.upper()

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, new_key: str):
        if len(new_key) <= 0:
            raise ValueError
        self._key = new_key.upper()

    @staticmethod
    def key_enlargment(text, key):
        key = key * math.ceil(len(text) / len(key))
        return key[:len(text)]

    # Encrypted char = (Plaintext + key) % 26
    def cipher(self, text: str) -> str:
        assert len(text) > 0

        # convert data to lowercase/uppercase
        text = text.upper()

        # adjust key length to text length
        new_key = self.key_enlargment(text, self.key)

        encrypted_string = []
        for i in range(len(text)):
            if text[i].isalpha():
                x = (ord(text[i]) + ord(new_key[i])) % 26
                x += ord('A')
                encrypted_string.append(chr(x))
            else:
                encrypted_string.append(text[i])
        return "".join(encrypted_string)

    # Decrypted char = (Encrypted - key) % 26
    def decipher(self, text: str) -> str:
        assert len(text) > 0

        # convert data to lowercase/uppercase
        text = text.upper()

        # adjust key length to text length
        new_key = self.key_enlargment(text, self.key)

        decrypted_string = []
        for i in range(len(text)):
            if text[i].isalpha():
                x = (ord(text[i]) - ord(new_key[i]) + 26) % 26
                x += ord('A')
                decrypted_string.append(chr(x))
            else:
                decrypted_string.append(text[i])
        return "".join(decrypted_string)
