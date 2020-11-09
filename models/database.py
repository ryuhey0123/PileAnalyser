from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
ENGINE = create_engine('sqlite:///' + DATABASE, convert_unicode=True, echo=True)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))

Base = declarative_base()
Base.query = session.query_property()


def init_db():
    from . import models
    Base.metadata.create_all(bind=ENGINE)
