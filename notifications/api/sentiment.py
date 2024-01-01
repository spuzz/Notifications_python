
from fastapi import APIRouter
import database.crud as crud, database.models as models, database.schemas as schemas
from utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
from transformers import pipeline

router = APIRouter(
    prefix="/sentiment",
    tags=["sentiment"],
)

logger = logging_api.get_app_logger("sentiment")

logger.info("Loading sentinment analysis model")
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

@router.get("/{post_id}")
def read_post_sentiment(post_id: str, db: Session = Depends(crud.get_db)):
    logger.info(f"Reading sentinment for post {post_id}")
    userpost = crud.get_userpost(db, id=post_id)
    text_list = []
    
    for i in userpost.comments:
        text_list.append(i.commentText)
    return sentiment_analysis(text_list)
    

def sentiment_analysis(text_list: list[str]):
    logger.info(f"Inference using sentiment model")
    result = 0
    for i in text_list:
        score = sentiment_pipeline(i)[0]["score"]
        result += score
    
    result = result / len(text_list)
    
    if result == 0:
        return "No Reaction"
    elif result <= 0.4:
        return "Negative Reaction"
    elif result >= 0.6:
        return "Positive Reaction"
    else:
        return "Mixed or Neutral Reaction"