from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_schemadisplay import create_schema_graph

from src.log import Logger

Base = declarative_base()
Session = sessionmaker()


class Database:

    def __init__(self, engine):
        self.engine = engine
        Base.metadata.bind = engine
        Session.configure(bind=engine)
        self.session = Session()

    def add_entry(self, entry):
        self.session.add(entry)
        self.commit_changes()
        Logger.log(entry, "Added")

    def add_entries(self, entries):
        self.session.add_all(entries)
        self.commit_changes()
        Logger.log(type(entries[0]), f"Added {len(entries)} new entries")

    def remove_entry(self, entry):
        self.session.delete(entry)
        self.commit_changes()
        Logger.log(entry, "Removed")

    @staticmethod
    def create_tables():
        Base.metadata.create_all()

    @staticmethod
    def create_schema_image():
        graph = create_schema_graph(metadata=MetaData('sqlite:///bot.db'),
                                    show_datatypes=True,  # The image would get nasty big if we'd show the datatypes
                                    show_indexes=False,  # ditto for indexes
                                    rankdir='LR',  # From left to right (instead of top to bottom)
                                    concentrate=False  # Don't try to join the relation lines together
                                    )

        graph.write_png('schema.png')

    def commit_changes(self):
        try:
            self.session.commit()
        except Exception as error:
            if self.engine.connection_invalidated:
                Logger.log("Database", "Reconnecting")
                self.engine.connect()

            self.session.rollback()
            raise error
