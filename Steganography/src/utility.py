from typing import Union
import numpy as np
import logging
import cv2


def encrypt_message(image, message):
    image = cv2.imread(image)
    # How many bytes we can encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    logging.info("Maximum bytes to encode: ", n_bytes)

    if len(message) > n_bytes:
        raise ValueError("Insufficient number of bytes, need bigger image or less data")

    # Delimiter
    message += "#" * 5
    message_index = 0

    # convert to binary
    binary_message = message_to_binary(message)
    # size of data to hide
    binary_message_len = len(binary_message)

    for row in image:
        for pixel in row:
            # Get RGB values of pixel
            r, g, b = message_to_binary(pixel)
            # rgb_array = [r,g,b]

            # modify LSB only if there is still data to store
            # for i, x in enumerate(rgb_array):
            #     if message_index < binary_message_len:
            #         pixel[i] = int(x[:-1] + binary_message[message_index], 2)
            #     elif message_index >= binary_message_len:
            #         break

            # modify LSB only if there is still data to store
            if message_index < binary_message_len:
                pixel[0] = int(r[:-1] + binary_message[message_index], 2)
                message_index += 1
            if message_index < binary_message_len:
                pixel[1] = int(g[:-1] + binary_message[message_index], 2)
                message_index += 1
            if message_index < binary_message_len:
                pixel[2] = int(b[:-1] + binary_message[message_index], 2)
                message_index += 1
            print(str(bin(pixel[0]))[-1] + str(bin(pixel[1]))[-1] + str(bin(pixel[2]))[-1])
            # find a way to end this loop or reduce number of if
            if message_index >= binary_message_len:
                break

    return image


def decrypt_message(image):
    image = cv2.imread(image)

    binary_message = ""
    for rows in image:
        for pixel in rows:
            r, g, b = message_to_binary(pixel)
            # rgb_array = [r,g,b]

            # for x in rgb_array:
            #     binary_data += x[-1]

            print(r)

            binary_message += r[-1]
            binary_message += g[-1]
            binary_message += b[-1]

            print(binary_message)

        all_bytes = [binary_message[i: i + 8] for i in range(0, len(binary_message), 8)]

        decoded_message = ""
        for byte in all_bytes:
            decoded_message += chr(int(byte, 2))
            if decoded_message[-5:] == "#" * 5:
                break

        return decoded_message[:-5]


def message_to_binary(message: Union[str, bytes, np.ndarray, int, np.uint8]):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message ])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")