from sqlalchemy import Table, Column, Integer, String
from database import metadata  # Change from .database to database

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100)),
    Column("email", String(100)),
)
