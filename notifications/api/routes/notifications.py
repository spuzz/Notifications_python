"""\
/notifications route endpoints

Handles api calls to create and retrieve like/comment notifications
"""

from fastapi import APIRouter
import api.database.crud as crud, api.database.models as models, api.database.schemas as schemas
from api.utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
from api.dependencies import get_db

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)

logger = logging_api.get_app_logger("notifications")

@router.post("/", response_model=schemas.UserPost)
def create_notification(notification: schemas.Notification, db: Session = Depends(get_db)):
    logger.info(f"Create notification from user {notification.user.id}") 
    db_post = parse_notification(notification,db)
    return db_post

@router.post("/list/", response_model=list[schemas.Notification])
def create_notifications(notifications: list[schemas.Notification], db: Session = Depends(get_db)):
    logger.info(f"Create multiple notifications from list")
    for i in notifications:
        parse_notification(i,db)
    return notifications

@router.get("/feed/{user_id}", response_model=list[str])
def get_notification_feed(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"Get notification feed for user {user_id}")
    db_user = crud.get_user(db, id=user_id)
    if db_user == None:
        logger.error(f"Could not find user {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    return get_notification_feed_by_post(db_user)


def parse_notification(notification: schemas.Notification, db: Session = Depends(get_db)):    
    # Check if user exists, real world application would error however, this example we create
    # the user if it does not exist and log a warning
    db_user = crud.get_user(db, id=notification.user.id)
    if db_user == None:
        logger.warning(f"No user {notification.user.id} exists, creating new user")
        db_user = crud.create_user(db=db, user=notification.user)
    # Check if post exists, real world application would error however, this example we create
    # the post if it does not exist and log a warning
    db_post = crud.get_userpost(db, id=notification.post.id)
    if db_post == None:
        logger.warning(f"No post {notification.post.id} exists, creating new post")
        db_post = crud.create_userpost(db=db, post=notification.post, user_id = "default")
    
    if notification.type == "Like":
        logger.info(f"Create like notification")
        db_like = crud.get_like(db, owner_id=notification.user.id, post_id=notification.post.id)
        # Handle resubmission of the same notification by returning a 409
        if db_like != None:
            raise HTTPException(status_code=409, detail="Notification already exists")
        crud.create_like(db=db, user_id = db_user.id, post_id = db_post.id, owner_name=db_user.name)
    elif notification.type == "Comment":
        logger.info(f"Create comment notification")
        
        # Handle comment type with no comment attached
        if notification.comment == None:
            raise HTTPException(status_code=422, detail="No Comment in payload")
        db_comment = crud.get_comment(db, id=notification.comment.id)
        # Handle resubmission of the same notification by returning a 409
        if db_comment != None:
            raise HTTPException(status_code=409, detail="Notification already exists")
        crud.create_comment(db=db, comment=notification.comment, user_id = db_user.id, post_id = db_post.id, owner_name=db_user.name)
    db_post = crud.get_userpost(db, id=db_post.id)
    return db_post


# Function to retrieve aggregated notification feed in text form (rather than user json)
def get_notification_feed_by_post(user: schemas.User):
    notifications = []
    for post in user.user_posts:
        logger.debug(f"Get notifications feed for post {post.id}")
        notification = get_like_notification_feed(post.likes, post=post)
        if notification != "":
            notifications.append(notification)  
        notification = get_comment_notification_feed(post)
        if notification != "":
            notifications.append(notification)  
    return notifications

# Function to create appropriate text feed from all comments on a post
def get_comment_notification_feed(post):
    notification = ""
    logger.debug(f"Number of comments: {len(post.comments)}")
    # if a single user commented then we add that users comment on the feed else we add the actual post
    if len(post.comments) == 1:
        notification = f'{post.comments[0].owner_name} commented on your post: "{post.comments[0].commentText}"'
    elif len(post.comments) == 2:
        notification = f'{post.comments[0].owner_name} and {post.comments[1].owner_name} commented on your post: "{post.title}"'
    elif len(post.comments) == 3:
        notification = f'{post.comments[0].owner_name}, {post.comments[1].owner_name} and 1 other commented on your post: "{post.title}"'
    elif len(post.comments) > 3:
        notification = f'{post.comments[0].owner_name}, {post.comments[1].owner_name} and {len(post.comments) - 2} others commented on your post: "{post.title}"'

    return notification

# Function to create appropriate text feed from all likes on a post
def get_like_notification_feed(likes, post = None):

    post_text = f': "{post.title}"'
    notification = ""
    logger.debug(f"Number of likes: {len(post.comments)}")
    if len(likes) == 1:
        notification = f'{likes[0].owner_name} liked your post{post_text}'
    elif len(likes) == 2:
        notification = f'{likes[0].owner_name} and {likes[1].owner_name} liked your post{post_text}'
    elif len(likes) == 3:
        notification = f'{likes[0].owner_name}, {likes[1].owner_name} and 1 other liked your post{post_text}'
    elif len(likes) > 3:
        notification = f'{likes[0].owner_name}, {likes[1].owner_name} and {len(likes) - 2} others liked your post{post_text}'

    return notification
