from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite база данных
engine = create_engine('sqlite:///nft_arbitrage.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Инициализировать базу данных"""
    import models
    Base.metadata.create_all(bind=engine)
