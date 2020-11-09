from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
    'user': 'ryuhey',  # createuser -P ryuhey
    'password': 'macmac',
    'host': 'localhost',
    'name': 'pile-analyser'  # createdb Test -O ryuhey
})

ENGINE = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, convert_unicode=True)

SessionMaker = sessionmaker(ENGINE)
Sess: Session = SessionMaker()

Base = declarative_base()
