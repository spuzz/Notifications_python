from fastapi import APIRouter
import database.crud as crud, database.models as models, database.schemas as schemas
from utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

logger = logging_api.get_app_logger("posts")

@router.get("/{post_id}", response_model=schemas.UserPost)
def read_userpost(post_id: str, db: Session = Depends(crud.get_db)):
    logger.info(f"Retrive post {post_id}")
    userpost = crud.get_userpost(db, id=post_id)
    return userpost