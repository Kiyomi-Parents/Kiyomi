from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.log import Logger

Base = declarative_base()
Session = sessionmaker()


class Database:

    def __init__(self, engine):
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        self.session = Session()

    def add_entry(self, entry):
        self.session.add(entry)
        Logger.log(entry, "Added")
        self.commit_changes()

    def add_entries(self, entries):
        self.session.add_all(entries)
        Logger.log(type(entries[0]), f"Added {len(entries)} new entries")
        self.commit_changes()

    def commit_changes(self):
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
