from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class BlogItem(BaseModel):
    name: str
    value: str
    type: int
    created_at :int
    updated_at :int
    blog_id : str

    