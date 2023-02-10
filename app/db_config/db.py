import os

from sqlalchemy import MetaData, create_engine

conn_str = (
    f'mysql+pymysql://{os.getenv("MYSQL_USERID")}:{os.getenv("MYSQL_PASSWORD")}',
    f'@{os.getenv("MYSQL_IP")}:{os.getenv("MYSQL_PORT")}/{os.getenv("MYSQL_DATABASE")}',
)

engine = create_engine(conn_str)
meta = MetaData()
conn = engine.connect()
