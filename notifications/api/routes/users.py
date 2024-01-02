"""\
/user route endpoints

Handles api calls to create and retrieve users
"""

from fastapi import APIRouter
import api.database.crud as crud, api.database.models as models, api.database.schemas as schemas
from api.utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
from api.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

logger = logging_api.get_app_logger("users")

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Create user {user.id}")
    db_user = crud.get_user(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=409, detail="User already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}" )
def read_user(user_id: str, db: Session = Depends(get_db)):
    logger.info(f"Retrieve user {user_id}")
    db_user = crud.get_user(db, id=user_id)
    if db_user == None:
        logger.error(f"Could not find user {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
