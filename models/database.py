import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


SQLITE_DATABASE_URL = 'sqlite:///' \
    + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')

POSTGRESQL_DATABASE_URL = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
    'user': 'ryuhey',  # createuser -P ryuhey
    'password': 'ryuhey',
    'host': 'localhost',
    'name': 'pile-analyser'  # createdb pile-analyser -O ryuhey
})

DATABASE_URL = SQLITE_DATABASE_URL
# DATABASE_URL = POSTGRESQL_DATABASE_URL

ENGINE = create_engine(DATABASE_URL, echo=False, convert_unicode=True, connect_args={'check_same_thread': False})

SessionMaker = sessionmaker(ENGINE)
Sess: Session = SessionMaker()

Base = declarative_base()
