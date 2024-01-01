from fastapi.testclient import TestClient

from main import app

import json
client = TestClient(app)


def test_read_main():

    sample_payload = {
        "id": "5497afbf9df3f6ff6f9ba11cdef5310f",
        "name": "Testy_McTestFace",
        "avatar": "test.jpg"
    }

    response = client.post("/users/", json=sample_payload)
    
    x = {
        'id': '5497afbf9df3f6ff6f9ba11cdef5310f',
        'name': 'Testy_McTestFace',
        'avatar': 'test.jpg',
        'user_posts': [],
        'user_comments': [],
        'user_likes': [] } 
    jsontest = json.dumps( x)
    assert response.status_code == 200
    assert json.dumps( response.json()) == jsontest

    x = {
        'id': '5497afbf9df3f6ff6f9ba11cdef5310f',
        'name': 'Testy_McTestFace',
        'avatar': 'test.jpg'
    }
    jsontest = json.dumps( x)
    response = client.get("/users/5497afbf9df3f6ff6f9ba11cdef5310f")
    print(json.dumps( response.json()))
    assert response.status_code == 200
    assert json.dumps( response.json()) == jsontest

def test_create_like():
    sample_payload= {
            "type" : "Like",
            "user": {
                "id": "403f220c3d413fe9cb0b36142ebfb35d",
                "name": "Mary T. Price",
                "avatar": None
            },
            "post": {
                "id": "b1638f970c3ddd528671df76c4dcf13e",
                "title": "Acme Inc dynamically scales niches worldwide"
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 200

def test_create_comment():
    sample_payload= {
            "type": "Comment",
            "post": {
                "id": "c4cfbe322bb834ada81719036f9b287b",
                "title": "How to distinctively leverage existing wireless ROI"
            },
            "comment":{
                "id": "9c6adba459bca33ee8ae81e4b1ca420c",
                "commentText": "True! And after that they should functionalize core competencies"
            },
            "user":{
                "id": "7305d0a8bb9d7166b8d26ca856930b8d",
                "name": "Ali Sage",
                "avatar": "portrait_02.png"
            }
        }
    response = client.post("/notifications/", json=sample_payload)
    assert response.status_code == 200

def test_read_userpost():
    response = client.get("/userposts/b1638f970c3ddd528671df76c4dcf13e")
    
    assert response.status_code == 200

def test_sentiment_userpost():
    response = client.get("/userposts/sentiment/c4cfbe322bb834ada81719036f9b287b")
    
    assert response.status_code == 200