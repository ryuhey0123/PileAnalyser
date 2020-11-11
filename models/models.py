import datetime
from hashlib import sha256

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    contents = relationship("Content", backref="users")
    projects = relationship("Project", backref="users")

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = str(sha256(password.encode("utf-8")).digest())
        self.timestamp = datetime.datetime.now()


class LoginUser(UserMixin, User):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    title = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    contents = relationship("Content", backref="projects")

    def __init__(self, title: str, user_id: int) -> None:
        self.title = title
        self.timestamp = datetime.datetime.now()
        self.user_id = user_id


class Soildata(Base):
    __tablename__ = 'soildatum'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    data = Column(JSON)

    contents = relationship("Content", backref="soildatum")

    def __init__(self, data: dict) -> None:
        self.data = data
        self.timestamp = datetime.datetime.now()


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    title = Column(String, nullable=True)

    input = Column(JSON, nullable=False)
    # output = Column(JSON, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project')

    soildata_id = Column(Integer, ForeignKey('soildatum.id'))
    soildata = relationship('Soildata')

    def __init__(self, title: str, input: dict, user_id: int, project_id: int, soildata_id: int):
        self.title = title
        self.input = input

        self.user_id = user_id
        self.project_id = project_id
        self.soildata_id = soildata_id

        self.timestamp = datetime.datetime.now()
