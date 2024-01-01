from sqlalchemy.orm import Session

import database.models as models, database.schemas as schemas
from database.database import SessionLocal, engine
from utils import logging_api


logger = logging_api.get_app_logger("database")
logger.info("Notification Feed Application initialising")

#
# Dependency
def get_db():
    logger.debug("Retrieving database connection")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_user(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if user.name == "":
        user.name = "User"
    db_user = models.User(id=user.id, name=user.name, avatar=user.avatar)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_userpost(db: Session, id: str):
    return db.query(models.UserPost).filter(models.UserPost.id == id).first()

def create_userpost(db: Session, post: schemas.UserPostCreate, user_id: int):
    db_post = models.UserPost(id=post.id, title=post.title, owner_id = user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, post_id: int, owner_name: str):
    db_comment = models.Comment(id=comment.id, commentText=comment.commentText, owner_id = user_id, post_id= post_id, owner_name = owner_name)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_like(db: Session, user_id: int, post_id: int, owner_name: str):
    db_like = models.Like(owner_id = user_id, post_id= post_id, owner_name = owner_name)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like