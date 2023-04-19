from ..db import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('NOW()'), nullable=False)
    user = Relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('NOW()'), nullable=False)
    phone_number = Column(String, nullable=False)


class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)