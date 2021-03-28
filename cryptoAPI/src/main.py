from fastapi import FastAPI
from symetric import Symetric
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64

symmetric = Symetric()

app = FastAPI()


# TODO: Refactor this to seperate files and modules this is just proof of concept

@app.get("/asymmetric/key")
async def get_asymmetric_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())

    public_key = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return {'private_key': base64.urlsafe_b64decode(private_key[27:-26].decode('UTF-8').replace('\n', '')).hex(),
            # using splitlines is also a valid option but converting to string and back is funnier :)
            'public_key': bytes(public_key[26:-25].decode('UTF-8').replace('\n', ''), "utf-8").hex()}


@app.get('/asymmetric/key/ssh')
async def get_ssh_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption())
    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )
    return {'private_key_ssh': base64.urlsafe_b64decode(private_key[27:-26].decode('UTF-8').replace('\n', '')).hex(),
            'public_key_ssh': public_key[8:].hex()}


@app.get("/symmetric/key")
async def get_symmetric_key():
    return {'key_hex': base64.urlsafe_b64decode(Fernet.generate_key()).hex()}


@app.post("symmetric/key")
async def post_symmetric_key(key: str):
    return None


@app.post("symmetric/encode")
async def encode(message: str):
    return None


@app.post("symmetric/decode")
async def decode(message: str):
    return None

# @app.post("asymmetric/key")
# async def post_asymmetric_key():
#     return None
#
#
# @app.post("asymmetric/verify")
# async def verify_message():
#     return None
#
#
# @app.post("asymmetric/sign")
# async def sign_message():
#     return None
#
#
# @app.post("asymmetric/encode")
# async def asymmetric_encode():
#     return None
#
#
# @app.post("asymmetric/decode")
# async def asymmetric_decode():
#     return None
