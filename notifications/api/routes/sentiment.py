"""\
/sentiment route endpoints

Handles API to sentiment analysis DL model which analyses the comments on the post to determine
the kind of reaction the post is receiving

The model returns a label for negative, neutral or positive and a value based on the estimated accuracy of the 
decision. This simple method add these up and returns the reaction with the highest score.
"""
from fastapi import APIRouter
import api.database.crud as crud, api.database.models as models, api.database.schemas as schemas
from api.utils import logging_api
from fastapi import Depends, FastAPI, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session 
from transformers import pipeline
from api.dependencies import get_db

router = APIRouter(
    prefix="/sentiment",
    tags=["sentiment"],
)

logger = logging_api.get_app_logger("sentiment")

logger.info("Loading sentinment analysis model")
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

@router.get("/{post_id}")
def read_post_sentiment(post_id: str, db: Session = Depends(get_db)):
    logger.info(f"Reading sentinment for post {post_id}")
    post = crud.get_userpost(db, id=post_id)
    if post == None:
        logger.error(f"Could not find post {post_id}")
        raise HTTPException(status_code=404, detail="Post not found")
    text_list = []
    
    for i in post.comments:
        text_list.append(i.commentText)
    # Not all posts have comments so need to exit out before passing empty list to model
    if len(text_list) == 0:
        return "No Reaction"
    return sentiment_analysis(text_list)
    

# Function to infer the reaction to a user posts using DL sentiment analysis model
def sentiment_analysis(text_list: list[str]):
    logger.info(f"Inference using sentiment model")
    scores = {"NEG": 0, "POS": 0, "NEU": 0}
    result = 0
    # Submit to DL model
    output = sentiment_pipeline(text_list)
    for i in output:
        # for each comment add score to the inferred reaction
        score = i["score"]
        label = i["label"]
        scores[label] += score
    
    # Highest scoring label is used 
    result = max(scores, key=scores.get)
    logger.debug(f"result from inference: {result}")

    if result == "NEG":
        return "Negative Reaction"
    elif result == "POS":
        return "Positive Reaction"
    else:
        return "Neutral Reaction"