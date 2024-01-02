"""\
Run unit tests on notification feed app

Run using pytest from root folder
"""


from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from main import sentiment
import json
import os

# Initialise by overriding the get_db function to call the test database instead of the "production" db
from api.database.database import Base
os.environ['RUN_ENV'] = 'test'
from main import app  # Import only after env created

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


# Calls the test db session instead of the default
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


############################################
#          Internal function Tests         #
############################################

# Test that the pretrained DL model produces reasonable outputs
def test_sentiment_analysis():
    assert sentiment.sentiment_analysis(["I love this"]) == "Positive Reaction"
    assert sentiment.sentiment_analysis(["I hate this"]) == "Negative Reaction"
    assert sentiment.sentiment_analysis(["I am not for or against this"]) == "Neutral Reaction"


############################################
#               API Tests                  #
############################################

# In real world example the test db would be cleared out to avoid invalid data however, for simplicity these
# tests will just check if the data already exists and consider that a pass
    
# Happy Path

# Test creation of a user
def test_create_user():
    sample_payload = {
        "id": "TestCreateUser",
        "name": "Created Tester",
        "avatar": "test.jpg"
    }

    response = client.post("/users/", json=sample_payload)
    
    assert response.status_code == 200 or response.status_code == 409

# Test retrieval of a user
def test_read_user():
    response = client.get("/users/TestUser")
    assert response.status_code == 200
    print(response.json())
    assert response.json()['id'] == 'TestUser'

# Test creation of a like notification and associated user and post
def test_create_like():
    sample_payload= {
            "type" : "Like",
            "user": {
                "id": "TestCreatedLikeUser",
                "name": "Test like user",
                "avatar": None
            },
            "post": {
                "id": "TestCreateLikePost",
                "title": "Test Post"
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 200 or response.status_code == 409

# Test creation of a comment notification and associated user and post
def test_create_comment():
    sample_payload= {
            "type": "Comment",
            "post": {
                "id": "TestCreateCommentPost",
                "title": "Test Post"
            },
            "comment":{
                "id": "TestCreateComment",
                "commentText": "Test Comment"
            },
            "user": {
                "id": "TestCreateCommentUser",
                "name": "Test like user",
                "avatar": None
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 200 or response.status_code == 409

# Test retrieval of a post
def test_read_userpost():
    response = client.get("/posts/TestPost")
    
    assert response.status_code == 200
    
# Test sentiment analysis of a post using pretrained DL model 
def test_sentiment_userpost():
    response = client.get("/sentiment/TestPost")
    
    assert response.json() == "Neutral Reaction"


# Unhappy Path
    
# Test creation of user with invalid payload fail correctly
def test_create_user_invalid():
    sample_payload = {
        "id_invalid": "TestUser",
        "name": "Testy_McTestFace",
        "avatar": "test.jpg"
    }

    response = client.post("/users/", json=sample_payload)
    
    assert response.status_code == 422

# Test retrieval of invalid user fails correctly
def test_read_user_invalid():
    response = client.get("/users/InvalidUser")
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'

# Test creation of like notification with invalid payload fail correctly
def test_create_like_invalid():
    sample_payload= {
            "type_invalid" : "Like",
            "user": {
                "id": "TestLikeUser",
                "name": "Test like user",
                "avatar": None
            },
            "post": {
                "id": "TestPost",
                "title": "Test Post"
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 422

# Test creation of comment notification with invalid payload fail correctly
def test_create_comment_invalid():
    sample_payload= {
            "type": "Comment",
            "post": {
                "id": "TestPost",
                "title": "Test Post"
            },
            "comment_invalid":{
                "id": "TestComment",
                "commentText": "Test Comment"
            },
            "user": {
                "id": "TestCommentUser",
                "name": "Test like user",
                "avatar": None
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 422

# Test retrieval of invalid post fail correctly
def test_read_userpost_invalid():
    response = client.get("/posts/InvalidPost")
    
    assert response.status_code == 404
    
# Test sentiment analysis of invalid post fail correctly
def test_sentiment_userpost_invalid():
    response = client.get("/sentiment/InvalidPost")
    
    assert response.status_code == 404