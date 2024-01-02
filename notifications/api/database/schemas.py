"""\
Pydantic schemas for fastapi and sqlalchemy integration with notification feed app


"""

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    id: str
    commentText: str | None = None
    model_config = ConfigDict(from_attributes=True)

class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    
    owner_id: str
    post_id: str
    owner_name: str

        


class LikeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    owner_id: str
    post_id: str
    owner_name: str
    

    
class UserPostBase(BaseModel):
    id: str
    title: str | None = None
    model_config = ConfigDict(from_attributes=True)

class UserPostCreate(UserPostBase):
    pass


class UserPost(UserPostBase):
    owner_id: str

    comments: list[Comment] = []
    likes: list[Like] = []



class UserBase(BaseModel):
    id: str
    name: str
    avatar: str | None = None
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass


class User(UserBase):
    user_posts: list[UserPost] = []
    user_comments: list[Comment] = []
    user_likes: list[Like] = []



class NotificationBase(BaseModel):
    type: str
    user: UserCreate
    post: UserPostCreate
    comment: CommentCreate | None = None
    model_config = ConfigDict(from_attributes=True)

class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):
    pass