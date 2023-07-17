from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostLike(BaseModel):
    Post_id: str
    Company_id: str
    Datetime: datetime


class PostLikeUpdate(BaseModel):
    Post_id: Optional[str]
    Company_id: Optional[str]
    Datetime: Optional[datetime]
