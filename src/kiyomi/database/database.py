from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.log import Logger

Base = declarative_base()
Session = sessionmaker()


class Database:

    def __init__(self, engine: Engine):
        self.engine = engine
        Base.metadata.bind = engine
        Session.configure(bind=engine)
        self.session = Session()

    @staticmethod
    def create_tables():
        Base.metadata.create_all()
        Logger.log("Database", f"Created {len(Base.metadata.tables)} tables")

    @staticmethod
    def drop_tables():
        Base.metadata.drop_all()
        Logger.log("Database", f"Dropped all database tables!")
