from sqlalchemy import create_engine, Column, Integer, String, Binary, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///test.db")

Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)

    name = Column(String)
    username = Column(String)
    email = Column(String)
    description = Column(String)

    password_hash = Column(Binary)

    visits = Column(Integer)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, Sequence("post_id_seq"), primary_key=True)

    title = Column(String)
    text = Column(String)

    by_user = Column(Integer, ForeignKey("user.id"))


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, Sequence("like_id_seq"), primary_key=True)

    by_user = Column(Integer, ForeignKey("user.id"))
    for_post = Column(Integer, ForeignKey("post.id"))


if __name__ == '__main__':
    User.__table__.create(checkfirst=True)
    Post.__table__.create(checkfirst=True)
    Like.__table__.create(checkfirst=True)

    print(Like.__table__.columns)
