from models.models import *
from models.database import Base, Sess, ENGINE


if __name__ == "__main__":
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all(bind=ENGINE)

    Sess.add(User(name='admin', password='admin'))

    user: User = Sess.query(User).filter(User.name == "admin").first()

    Sess.add(Project(title='Sample Project1', user_id=user.id))
    Sess.add(Project(title='Sample Project2', user_id=user.id))

    Sess.commit()
