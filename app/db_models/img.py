from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import INTEGER, String, VARCHAR
from ..db_config.db import meta, engine


imgs = Table('img', meta,
              Column('id', VARCHAR(100), primary_key=True),
              Column('input_path', VARCHAR(100)),
              Column('output_path', VARCHAR(100)),
              )

meta.create_all(engine)