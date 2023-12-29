from pydantic import BaseModel


class CommentBase(BaseModel):
    id: str
    commentText: str | None = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    
    owner_id: str
    post_id: str

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    pass


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    owner_id: str
    post_id: str

    class Config:
        orm_mode = True

    
class UserPostBase(BaseModel):
    id: str
    title: str | None = None


class UserPostCreate(UserPostBase):
    pass


class UserPost(UserPostBase):
    owner_id: str

    comments: list[Comment] = []
    likes: list[Like] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str
    name: str
    avatar: str | None = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_posts: list[UserPost] = []
    user_comments: list[Comment] = []
    user_likes: list[Like] = []

    class Config:
        orm_mode = True


class NotificationBase(BaseModel):
    type: str
    user: UserCreate
    post: UserPostCreate
    comment: CommentCreate | None = None

class NotificationCreate(NotificationBase):
    pass


class Notification(NotificationBase):

    class Config:
        orm_mode = True