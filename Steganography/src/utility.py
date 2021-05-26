from PIL import Image
from typing import Generator


def _validate_image(image: Image) -> None:
    """ Method of validating Image, only three modes is avaible and JPEG is not supported because compression.

    :param image: Image that we want to validate, PIL library is necessary
    """
    if image.mode not in ('RGB', 'RGBA', 'CMYK'):
        raise ValueError('Unsupported pixel format: '
                         'image must be RGB, RGBA, or CMYK')
    if image.format == 'JPEG':
        raise ValueError('JPEG format incompatible')


def encrypt_image_data(image_data, data: bytes) -> Generator[tuple, None, None]:
    """ Method for encrypting data into image

    :param image_data: Data of image
    :param data: Bytes that we want to encrypt
    """
    datalen = len(data)
    if datalen == 0:
        raise ValueError('data is empty')
    if datalen * 3 > len(image_data):
        raise ValueError('data is too large for image')

    image_data = iter(image_data)

    for i in range(datalen):
        pixels = [value & ~1 for value in
                  image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        byte = data[i]
        for j in range(7, -1, -1):
            pixels[j] |= byte & 1
            byte >>= 1
        if i == datalen - 1:
            pixels[-1] |= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]


def decrypt_image_data(image_data) -> Generator[chr, None, None]:
    """ Method for decrypting data from image

    :param image_data: Data of image
    """
    image_data = iter(image_data)
    while True:
        pixels = list(image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3])
        byte = 0
        for c in range(7):
            byte |= pixels[c] & 1
            byte <<= 1
        byte |= pixels[7] & 1
        yield chr(byte)
        if pixels[-1] & 1:
            break


def encrypt_inplace(image: Image, data:bytes) -> None:
    """ Method for encrypting Image in place

    :param image: Data of image
    :param data: Bytes that we want to encrypt
    """
    _validate_image(image)

    w = image.size[0]
    (x, y) = (0, 0)
    for pixel in encrypt_image_data(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

def encrypt_lossy(image: Image, data: bytes) -> None:
    # 8x8 chunks image splitting
    # Discrete cosine transform
    # LSB of all coefficients is changed to a bit taken from each 8-bit block message
    pass


def encrypt(image: Image, data: bytes) -> Image:
    """ Method for encrypting Image

    :param image: Data of image
    :param data: Bytes that we want to encrypt
    :return: Encrypted Image
    """
    image = image.copy()
    encrypt_inplace(image, data)
    return image


def decrypt(image: Image) -> str:
    """ Method for decrypting bytes from Image

    :param image: Data of image
    :return: decrypted bytes
    """
    _validate_image(image)

    return ''.join(decrypt_image_data(image.getdata()))
