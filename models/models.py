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

    contents = relationship("Content", backref="projects")

    def __init__(self, title: str) -> None:
        self.title = title
        self.timestamp = datetime.datetime.now()


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


if __name__ == "__main__":
    from sqlalchemy import create_engine, desc
    from sqlalchemy.orm import sessionmaker, Session

    # SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
        'user': 'ryuhey',  # createuser -P ryuhey
        'password': 'macmac',
        'host': 'localhost',
        'name': 'pile-analyser'  # createdb Test -O ryuhey
    })

    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    SessionMaker = sessionmaker(engine)
    session: Session = SessionMaker()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # ユーザー追加例 ----------------------------------------------------------------------------------------

    session.add(User(name='alice', password='fuckyou'))
    session.add(User(name='bob', password='thankyou'))

    test_project1 = Project(title='Test Project1')
    test_project2 = Project(title='Test Project2')
    session.add(test_project1)
    session.add(test_project2)

    # コンテンツ追加例 ---------------------------------------------------------------------------------------

    # まずユーザー名からアドレスをIDを検索する
    test_user: User = session.query(User).filter(User.name == 'alice').first()

    # そのIDを用いてContentインスタンスを追加する
    session.add(Content(
        user_id=test_user.id,
        project_id=test_project1.id,
        input={'diameter': 1300, 'length': 17.0},
        output={'x': [1, 2, 3], 'y': [3, 4, 5]}
    ))

    session.add(Content(
        user_id=test_user.id,
        project_id=test_project2.id,
        input={'diameter': 1800, 'length': 17.0},
        output={'x': [1, 2, 5], 'y': [3, 4, 5]}
    ))

    test_user: User = session.query(User).filter(User.name == 'bob').first()

    session.add(Content(
        user_id=test_user.id,
        project_id=test_project1.id,
        input={'diameter': 2000, 'length': 17.0},
        output={'x': [1, 2, 3], 'y': [3, 4, 5]}
    ))

    session.commit()

    # コンテンツ検索例 ---------------------------------------------------------------------------------------

    # ユーザーネームからUserインスタンスを探す
    user: User = session.query(User).filter_by(name='alice').first()
    # user_id を用いてコンテンツを検索し、最新のものを選択
    content: Content = session.query(Content).filter_by(user_id=user.id).order_by(desc('timestamp')).first()
    print(content.input.get('diameter'))
    project: Project = session.query(Project).filter_by(id=content.project_id).first()
    print(project.title)

    session.close()
