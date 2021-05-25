from PIL import Image


def _validate_image(image):
    if image.mode not in ('RGB', 'RGBA', 'CMYK'):
        raise ValueError('Unsupported pixel format: '
                         'image must be RGB, RGBA, or CMYK')
    if image.format == 'JPEG':
        raise ValueError('JPEG format incompatible')


def crypt_image_data(image_data, data):
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


def decrypt_image_data(image_data):
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


def crypt_inplace(image, data):
    _validate_image(image)

    w = image.size[0]
    (x, y) = (0, 0)
    for pixel in crypt_image_data(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def crypt(image, data):
    image = image.copy()
    crypt_inplace(image, data)
    return image


def decrypt(image):
    _validate_image(image)

    return ''.join(decrypt_image_data(image.getdata()))
