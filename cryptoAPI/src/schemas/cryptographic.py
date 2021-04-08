from typing import Optional, Union

from pydantic import BaseModel


class Cryptographic(BaseModel):
    privateKey: Optional[Union[bytes]] = None
    publicKey: Optional[Union[bytes]] = None
