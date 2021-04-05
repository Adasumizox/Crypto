import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

cryptoInfo = sqlalchemy.Table(
    "cryptoInfo",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("privateKey", sqlalchemy.Binary),
    sqlalchemy.Column("publicKey", sqlalchemy.Binary),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)