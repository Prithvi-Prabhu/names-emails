from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "mysql+aiomysql://root:1301@localhost/codeclub"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)
