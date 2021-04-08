import base64

import uvicorn as uvicorn
from cryptography.fernet import Fernet
from fastapi import FastAPI

from cryptoAPI.src.database.database import database, cryptoInfo
from cryptoAPI.src.api.api import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    await database.connect()
    current_keys = await database.fetch_all(cryptoInfo.select())
    if len(current_keys) < 1:
        query = cryptoInfo.insert().values(privateKey=base64.urlsafe_b64encode(Fernet.generate_key()))
        await database.execute(query)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()