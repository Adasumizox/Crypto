import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from fastapi import APIRouter, HTTPException

from cryptoAPI.src.database.database import database, cryptoInfo

router = APIRouter()


@router.get("/key")
async def get_asymmetric_key() -> object:
    """ Return asymmetric pair of keys with various formats and set them on server

    :return: asymmetric pair of keys
    """
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

    query = cryptoInfo.update() \
        .where(cryptoInfo.c.id == 1) \
        .values(privateKey=private_key, publicKey=public_key)
    await database.execute(query)

    return {'private_key': base64.urlsafe_b64decode(private_key[27:-26].decode('UTF-8').replace('\n', '')).hex(),
            'private_key_pem': private_key,
            # using splitlines is also a valid option but converting to string and back is funnier :)
            'public_key': bytes(public_key[26:-25].decode('UTF-8').replace('\n', ''), "utf-8").hex(),
            'public_key_pem': public_key}


@router.get('/key/ssh')
async def get_ssh_key() -> object:
    """ Return asymmetric pair of keys in SSH form

    :return: asymmetric pair of keys [SSH form]
    """
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


@router.post("/key")
async def post_asymmetric_key(key: dict):
    """ Set provided asymmetric pair of keys on server

    :param key: dictionary of two values [can be json] which must contain
    names private_key with private_key and public_key with public_key
    :return: Information about operation or HTTP exception
    """
    private_key = bytes(key['private_key'], 'utf-8')
    public_key = bytes(key['public_key'], 'utf-8')

    query = cryptoInfo.update() \
        .where(cryptoInfo.c.id == 1) \
        .values(privateKey=private_key, publicKey=public_key)
    last_record_id = await database.execute(query)

    if last_record_id != 1:
        raise HTTPException(status_code=500, detail="Server is unable to process this request,")
    return "Operation completed succesfully"


@router.post("/sign")
async def sign_message(message: str):
    """ Create signature of provided message

    :param message: message that we want to sign
    :return: signature that can be provided to check if message was modified
    """
    query = cryptoInfo.select()
    private_key = await database.fetch_val(query, column=cryptoInfo.c.privateKey)
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


@router.post("/verify")
async def verify_message(signature: str, message: str) -> object:
    """ Verify if message was altered using signature and message

    :param signature: signature of our message in base64 urlsafe form
    :param message: message that we want to check if was modified
    :return: status of verification or HTTPException if verification failed
    """
    query = cryptoInfo.select()
    public_key = await database.fetch_val(query, column=cryptoInfo.c.publicKey)
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


@router.post("/encode")
async def encode(message: str) -> object:
    """ Encode provided message

    :param message: message that we want to encode
    :return: encoded message
    """
    query = cryptoInfo.select()
    public_key = await database.fetch_val(query, column=cryptoInfo.c.publicKey)
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


@router.post("/decode")
async def decode(ciphertext: str) -> object:
    """ Decode provided ciphertext

    :param ciphertext: message base64 urlsafe encoded
    :return: decoded message
    """
    query = cryptoInfo.select()
    private_key = await database.fetch_val(query, column=cryptoInfo.c.privateKey)
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
