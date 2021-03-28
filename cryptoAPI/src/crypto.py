from pydantic import BaseModel
from typing import Optional


class Crypto(BaseModel):
    key: bytes = None
    text: Optional[str] = None
    ciphertext: Optional[str] = None
