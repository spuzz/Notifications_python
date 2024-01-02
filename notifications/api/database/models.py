"""\
Database models for notification feed app

database is built to allow users to both post and like/comments on others 
However for this example only the "default" user will have posts

"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    avatar = Column(String, index=True)
    user_posts = relationship("UserPost", back_populates="owner")
    user_comments = relationship("Comment", back_populates="owner")
    user_likes = relationship("Like", back_populates="owner")

class UserPost(Base):
    __tablename__ = "userposts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="user_posts")
    comments = relationship("Comment", back_populates="user_posts")
    likes = relationship("Like", back_populates="user_posts")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    commentText = Column(String, index=True)

    post_id = Column(String, ForeignKey("userposts.id"))
    owner_id = Column(String, ForeignKey("users.id"))

    owner_name = Column(String)

    user_posts = relationship("UserPost", back_populates="comments")
    owner = relationship("User", back_populates="user_comments")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(String, ForeignKey("users.id"))
    post_id = Column(String, ForeignKey("userposts.id"))

    owner_name = Column(String)

    user_posts = relationship("UserPost", back_populates="likes")
    owner = relationship("User", back_populates="user_likes")