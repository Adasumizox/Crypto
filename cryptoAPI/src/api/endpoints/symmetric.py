import base64
import re

from cryptography.fernet import Fernet
from fastapi import APIRouter, HTTPException

from cryptoAPI.src.database.database import database, cryptoInfo

router = APIRouter()


@router.get("/key")
async def get_symmetric_key() -> object:
    """ Return symmetric key

    :return: Symmetric key in hex and normal form
    """
    key = Fernet.generate_key()
    return {'key_hex': base64.urlsafe_b64decode(key).hex(),
            'key': key}


@router.post("/key")
async def post_symmetric_key(key: str) -> object:
    """ Set symmetric key in server

    :param key: 32 bit hexadecimal key
    :return: information about operation or exception
    """
    PATTERN = r"[0-9a-fA-F]+"

    if not re.fullmatch(PATTERN, key):
        raise HTTPException(status_code=422, detail="Data must be in hex format")
    if not len(key) == 32:
        raise HTTPException(status_code=422, detail="Data must contain 32 characters")

    query = cryptoInfo.update() \
        .where(cryptoInfo.c.id == 1) \
        .values(privateKey=base64.urlsafe_b64encode(bytes(key, 'UTF-8')))
    last_record_id = await database.database.execute(query)
    if last_record_id != 1:
        raise HTTPException(status_code=500, detail="Server is unable to process this request,")
    return "Operation completed succesfully"


@router.post("/encode")
async def encode(message: str) -> object:
    """ Encode provided message using symmetric cryptography

    :param message: message that we want to encode
    :return: encoded message
    """
    query = cryptoInfo.select()
    private_key = await database.fetch_val(query, column=cryptoInfo.c.privateKey)
    f = Fernet(private_key)
    return f.encrypt(bytes(message, "UTF-8"))


@router.post("/decode")
async def decode(message: str) -> object:
    """ Decode provided message using symmetric cryptography

    :param message: message that we want to decode
    :return: decoded message
    """
    query = cryptoInfo.select()
    private_key = await database.fetch_val(query, column=cryptoInfo.c.privateKey)
    f = Fernet(private_key)
    return f.decrypt(bytes(message, "UTF-8"))
