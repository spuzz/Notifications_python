from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
import json
from fastapi.testclient import TestClient
import database.crud as crud, database.models as models, database.schemas as schemas
from database.database import SessionLocal, engine
import contextlib
from sqlalchemy import MetaData
from utils import logging_api
from api import users, posts, notifications, sentiment

logger = logging_api.get_app_logger("main")
logger.info("Notification Feed Application initialising")
models.Base.metadata.create_all(bind=engine)

logger.info("Starting api")
app = FastAPI()

logger.info("Application started succesfully")

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(notifications.router)
app.include_router(sentiment.router)

@app.post("/uploadfile/")
async def upload_json_feed(upload_file: UploadFile = File(...), db: Session = Depends(crud.get_db)):
    json_data = json.load(upload_file.file)
    for i in json_data:
        notifications.parse_notification(schemas.Notification.parse_obj(i),db)
    return json_data

    
meta = models.Base.metadata

with contextlib.closing(engine.connect()) as con:
    trans = con.begin()
    for table in reversed(meta.sorted_tables):
        con.execute(table.delete())
    trans.commit()
client = TestClient(app)
sample_payload = {
    "id": "default",
    "name": "Testy_McTestFace",
    "avatar": None
}

response = client.post("/users/", json=sample_payload)