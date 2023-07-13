from pydantic import BaseModel
from datetime import datetime

class PostLike(BaseModel):
    Post_id: str
    Company_id: str
    Datetime: datetime
