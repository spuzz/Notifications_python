"""\
/posts route endpoints

Handles api calls to retrieve posts

Challenge doesn't require the creation of posts and therefore has been left out
"""

from fastapi import APIRouter
import api.database.crud as crud, api.database.models as models, api.database.schemas as schemas
from api.utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
from api.dependencies import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

logger = logging_api.get_app_logger("posts")

@router.get("/{post_id}", response_model=schemas.UserPost)
def read_userpost(post_id: str, db: Session = Depends(get_db)):
    logger.info(f"Retrieve post {post_id}")
    post = crud.get_userpost(db, id=post_id)
    if post == None:
        logger.error(f"Could not find post {post_id}")
        raise HTTPException(status_code=404, detail="Post not found")
    return post