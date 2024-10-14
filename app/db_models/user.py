from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import INTEGER, String

from ..db_config.db import engine, meta

users = Table(
    "users",
    meta,
    Column("id", INTEGER(), primary_key=True),
    Column("name", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
)


meta.create_all(engine)
