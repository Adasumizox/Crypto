import logging

logger = logging.getLogger("main")
logging.basicConfig(level=logging.DEBUG)


def hashing() -> None:
    from hashing.src.HashHelper import HashHelper
    from hashing.src.Transfer import Transfer

    logger.info(HashHelper.hashing_time_for_all_algorithms(text='password', loops=10000))
    name = Transfer.download_file("https://releases.ubuntu.com/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso")
    logger.info(HashHelper.compare_file_with_checksum("./{}".format(name),
                                                      "93bdab204067321ff131f560879db46bee3b994bf24836bb78538640f689e58f",
                                                      "sha256"))
    HashHelper.display_plot(
        HashHelper.generate_hash_size_times(length=1000000, algorithm="sha1", step=100000, loops=1000))


def hashing_passwords() -> None:
    from getpass import getpass

    from hashingPassword.src.HashPasswordHelper import HashPasswordHelper
    from hashingPassword.src.DatabaseController import DatabaseController

    DATABASE = './clients'

    username = input("Username: ")
    password = getpass("Password:")
    password2 = getpass("Repeat Password:")
    if password == password2:
        algorithm = None
        while algorithm is None:
            print("Please enter number of your prefered algorithm 1. SHA512 2. pbkdf2_hmac")
            preferred = int(input())
            if preferred == 1:
                algorithm = "SHA512"
            elif preferred == 2:
                algorithm = "PBKDF2_HMAC"
            else:
                print("Number not recognized please try again.")
        salt = HashPasswordHelper.generate_salt()
        password = HashPasswordHelper.hash_password(password, salt, algorithm)
        db = DatabaseController(DATABASE)
        db.create_user(username, password, salt, algorithm)
        logging.info(f"Is password from user and from database the same: "
                     f"{HashPasswordHelper.verify_password(DATABASE, username, password2)}")

    else:
        print("Passwords are not the same")


def api() -> None:
    import base64

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


def cipher() -> None:
    from MonoAl.src.Mono import Mono

    data = ""

    with open("./text.txt", "r") as file:
        data = file.read()

    mono = Mono(data)
    mono.transpose_column(4)
    logger.info(mono.cipher(None))


if __name__ == '__main__':
    cipher()