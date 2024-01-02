"""\
CRUD database access for notification feed app

Tables:
users
posts
comments
likes

"""

from sqlalchemy.orm import Session

import api.database.models as models, api.database.schemas as schemas
from api.database.database import SessionLocal, engine
from api.utils import logging_api


logger = logging_api.get_app_logger("database")
logger.info("Notification Feed Application initialising")

        
def get_user(db: Session, id: str):
    logger.debug(f"Get user {id} from database")
    return db.query(models.User).filter(models.User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    logger.debug(f"Get all users from database")
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # If no use user name was specified we add the name as "User"
    if user.name == "":
        user.name = "User"
    logger.debug(f"Creating user {user.id} in database")
    db_user = models.User(id=user.id, name=user.name, avatar=user.avatar)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_userpost(db: Session, id: str):
    logger.debug(f"Getting post {id}from database")
    return db.query(models.UserPost).filter(models.UserPost.id == id).first()

def create_userpost(db: Session, post: schemas.UserPostCreate, user_id: int):
    logger.debug(f"Creating post {post.id} in database")
    db_post = models.UserPost(id=post.id, title=post.title, owner_id = user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_like(db: Session, owner_id: str, post_id: str):
    logger.debug(f"Get like for user {owner_id} and post {post_id} from database")
    return db.query(models.Like).filter(models.Like.owner_id == owner_id and models.Like.post_id == post_id).first()

def get_comment(db: Session, id: str):
    logger.debug(f"Get comment {id} from database")
    return db.query(models.Comment).filter(models.Comment.id == id).first()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, post_id: int, owner_name: str):
    logger.debug(f"Creating comment for user {user_id} and post {post_id} in database")
    db_comment = models.Comment(id=comment.id, commentText=comment.commentText, owner_id = user_id, post_id= post_id, owner_name = owner_name)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_like(db: Session, user_id: int, post_id: int, owner_name: str):
    logger.debug(f"Creating like for user {user_id} and post {post_id} in database")
    db_like = models.Like(owner_id = user_id, post_id= post_id, owner_name = owner_name)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like