from sqlalchemy import create_engine, MetaData
engine = create_engine('mysql+pymysql://root:dlapdlf134!@34.64.170.250:3306/test_database')
meta = MetaData()
conn = engine.connect()