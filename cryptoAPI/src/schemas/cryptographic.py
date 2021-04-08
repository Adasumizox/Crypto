from typing import Optional

from pydantic import BaseModel


class Cryptographic(BaseModel):
    privateKey: Optional[bytes] = None
    publicKey: Optional[bytes] = None
