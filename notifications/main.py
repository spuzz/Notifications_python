from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session 

import crud, models, schemas
from database import SessionLocal, engine

import contextlib
from sqlalchemy import MetaData

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

meta = models.Base.metadata

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}" )
def read_users(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, id=user_id)
    return user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/userposts/{post_id}", response_model=schemas.UserPost)
def read_userpost(post_id: str, db: Session = Depends(get_db)):
    userpost = crud.get_userpost(db, id=post_id)
    return userpost

@app.post("/notifications/", response_model=schemas.UserPost)
def submit_notification(notification: schemas.Notification, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=notification.user.id)
    if db_user == None:
        db_user = crud.create_user(db=db, user=notification.user)
    db_post = crud.get_userpost(db, id=notification.post.id)
    if db_post == None:
        db_post = crud.create_userpost(db=db, post=notification.post, user_id = db_user.id)
    
    if notification.type == "Like":
        crud.create_like(db=db, user_id = db_user.id, post_id = db_post.id)
    elif notification.type == "Comment":
        crud.create_comment(db=db, comment=notification.comment, user_id = db_user.id, post_id = db_post.id)
    db_post = crud.get_userpost(db, id=db_post.id)
    return db_post


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}