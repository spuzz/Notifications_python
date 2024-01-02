
"""\
Fastapi entry point for notification feed app

This application was built for Phrasee notification feed challenge

The design assumes that a production version of this application would have users able to make
both posts and comment/like others posts. However, for the challenge we do not have the users
and posts in an active database and therefore create the posts and users when they are found within
the notification submissions.

We also create a "default" user as the challenge assumes only one notification feed for a single user

Run using "uvicorn main:app --reload"
"""

from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
import json
from fastapi.testclient import TestClient
import api.database.crud as crud, api.database.models as models, api.database.schemas as schemas
from api.database.database import engine
import contextlib
from sqlalchemy import MetaData
from api.utils import logging_api
from api.routes import users, posts, notifications, sentiment
from api.dependencies import get_db

logger = logging_api.get_app_logger("main")
logger.info("Notification Feed Application initialising")
models.Base.metadata.create_all(bind=engine)

logger.info("Starting api")

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(notifications.router)
app.include_router(sentiment.router)

logger.info("Application started succesfully")

# Single top level endpoint for uplaoding notification stream json file
# Will automatically create all relevant users, posts, likes and comments in database
@app.post("/uploadfile/")
def upload_json_feed(upload_file: UploadFile = File(...), db: Session = Depends(get_db)):
    json_data = json.load(upload_file.file)
    for i in json_data:
        try:
            notifications.parse_notification(schemas.Notification.parse_obj(i),db)
        except HTTPException as e:
            # Ignore duplication errors so that multiple uploads of the same file are ignored
            if e.status_code == 409:
                logger.warning("Notification already exists")
            else:
                raise e


    return json_data

# Production system would assume users are already created however, in this scenario we are manually
# adding a generic user to the database that will have written the posts
# If run a second time the below code will simply exit with no change
client = TestClient(app)
sample_payload = {
    "id": "default",
    "name": "Testy_McTestFace",
    "avatar": None
}

response = client.post("/users/", json=sample_payload)