from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    body = Column(String)

    creator = relationship('User', back_populates='blogs')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    blogs = relationship('Blog', back_populates='creator')
