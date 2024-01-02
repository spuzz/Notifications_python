# Notifications feed challenge using python
## Python and fastapi based application to process notifications and aggregate into a notification feed
### Creates a sqlite database to store the notification feed and aggregate by type and post. Uses deep learning sentiment analysis to estimate the reaction to a users post based on the notification feed comments.

Requirements
- fastapi
- pytest
- sqlalchemy
- transformers (hugging face)
- pytorch

<br>
Designed for a system with users able to both post and like/comment on other users posts. The current version assumes an incomplete database and will create a default user that all "posts" in the notification feed will be assigned and will create users/posts as the notification feed is parsed.
<br>
<br>
The aggregated feed can be retrieved from the /user/default (for default user) endpoint and will return a json containing a user with each post and its associated likes/comments. A front end UI could then display the results in text form.
<br>
<br>
Alternatively a separate endpoint /feed/default (for default user) endpoint will return an aggregated notification feed in text format to follow the example notification feed "Notification Test.png".
<br>
<br>
A pretrained model from hugging face model hub is used for inference of reactions to user posts.
<br>
The endpoint /sentiment/{post_id} will return text describing the estimated reaction to the post.
<br>
<br>
Run using "uvicorn main:app --reload" from the /notifications directory.
<br>
<br>
Once running, full API spec can be accessed from 127.0.0.1:8000/docs 
<br>
<br>
Unit tests written using pytest check the functionality of the API. These can be run using "pytest" in the notifications directory.
<br>

