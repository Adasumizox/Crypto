import base64
import re

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from fastapi import FastAPI, HTTPException

import database

app = FastAPI()


# TODO: Refactor this to seperate files and modules this is just proof of concept

@app.on_event("startup")
async def startup():
    await database.database.connect()
    current_keys = await database.database.fetch_all(database.cryptoInfo.select())
    if len(current_keys) < 1:
        query = database.cryptoInfo.insert().values(privateKey=base64.urlsafe_b64encode(Fernet.generate_key()))
        await database.database.execute(query)


@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()


@app.get("/symmetric/key")
async def get_symmetric_key():
    key = Fernet.generate_key()
    return {'key_hex': base64.urlsafe_b64decode(key).hex(),
            'key': key}


@app.post("/symmetric/key")
async def post_symmetric_key(key: str):
    PATTERN = r"[0-9a-fA-F]+"

    if not re.fullmatch(PATTERN, key):
        raise HTTPException(status_code=422, detail="Data must be in hex format")
    if not len(key) == 32:
        raise HTTPException(status_code=422, detail="Data must contain 32 characters")

    query = database.cryptoInfo.update() \
        .where(database.cryptoInfo.c.id == 1) \
        .values(privateKey=base64.urlsafe_b64encode(bytes(key, 'UTF-8')))
    last_record_id = await database.database.execute(query)
    if last_record_id != 1:
        raise HTTPException(status_code=500, detail="Server is unable to process this request,")
    return "Operation completed succesfully"


@app.post("/symmetric/encode")
async def encode(message: str):
    query = database.cryptoInfo.select()
    private_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.privateKey)
    f = Fernet(private_key)
    return f.encrypt(bytes(message, "UTF-8"))


@app.post("/symmetric/decode")
async def decode(message: str):
    query = database.cryptoInfo.select()
    private_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.privateKey)
    f = Fernet(private_key)
    return f.decrypt(bytes(message, "UTF-8"))


@app.get("/asymmetric/key")
async def get_asymmetric_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    )

    query = database.cryptoInfo.update() \
        .where(database.cryptoInfo.c.id == 1) \
        .values(privateKey=private_key, publicKey=public_key)
    await database.database.execute(query)

    return {'private_key': base64.urlsafe_b64decode(private_key[27:-26].decode('UTF-8').replace('\n', '')).hex(),
            'private_key_pem': private_key,
            # using splitlines is also a valid option but converting to string and back is funnier :)
            'public_key': bytes(public_key[26:-25].decode('UTF-8').replace('\n', ''), "utf-8").hex(),
            'public_key_pem': public_key}


@app.get('/asymmetric/key/ssh')
async def get_ssh_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH,
        serialization.PublicFormat.OpenSSH
    )
    return {'private_key_ssh': base64.urlsafe_b64decode(private_key[27:-26].decode('UTF-8').replace('\n', '')).hex(),
            'public_key_ssh': public_key[8:].hex()}


@app.post("/asymmetric/key")
async def post_asymmetric_key(key: dict):
    private_key = bytes(key['private_key'], 'utf-8')
    public_key = bytes(key['public_key'], 'utf-8')

    query = database.cryptoInfo.update() \
        .where(database.cryptoInfo.c.id == 1) \
        .values(privateKey=private_key, publicKey=public_key)
    last_record_id = await database.database.execute(query)

    if last_record_id != 1:
        raise HTTPException(status_code=500, detail="Server is unable to process this request,")
    return "Operation completed succesfully"


@app.post("/asymmetric/sign")
async def sign_message(message: str):
    query = database.cryptoInfo.select()
    private_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.privateKey)
    private_key = serialization.load_pem_private_key(private_key, password=None)
    message = bytes(message, 'utf-8')

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return {'signature_hex': str(signature.hex()),
            'signature_b64': str(base64.urlsafe_b64encode(signature))}


@app.post("/asymmetric/verify")
async def verify_message(signature: str, message: str):
    query = database.cryptoInfo.select()
    public_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.publicKey)
    public_key = serialization.load_pem_public_key(public_key)
    signature = base64.urlsafe_b64decode(signature)
    message = bytes(message, 'utf-8')

    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return "Verification completed"
    except:
        raise HTTPException(status_code=400, detail="Message verification failed")


@app.post("/asymmetric/encode")
async def encode(message: str):
    query = database.cryptoInfo.select()
    public_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.publicKey)
    public_key = serialization.load_pem_public_key(public_key)
    message = bytes(message, 'utf-8')

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(ciphertext)


@app.post("/asymmetric/decode")
async def decode(ciphertext: str):
    query = database.cryptoInfo.select()
    private_key = await database.database.fetch_val(query, column=database.cryptoInfo.c.privateKey)
    private_key = serialization.load_pem_private_key(private_key, password=None)
    ciphertext = base64.urlsafe_b64decode(ciphertext)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext