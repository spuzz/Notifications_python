from fastapi import APIRouter
import database.crud as crud, database.models as models, database.schemas as schemas
from utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

logger = logging_api.get_app_logger("users")

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(crud.get_db)):
    logger.info(f"Create user {user.id}")
    db_user = crud.get_user(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}" )
def read_user(user_id: str, db: Session = Depends(crud.get_db)):
    logger.info(f"Retrieve user {user_id}")
    user = crud.get_user(db, id=user_id)
    return user
