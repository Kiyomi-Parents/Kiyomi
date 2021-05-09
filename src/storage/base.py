from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create engine and configure session with engine
engine = create_engine('sqlite:///bot.db', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
