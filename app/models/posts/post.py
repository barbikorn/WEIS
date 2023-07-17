from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    Id: int
    Cat_id: int
    Datetime: datetime
    Post_type: int
    Waste_type: int
    Waste_code: str
    Qty: float
    Description: str
    Detail: str
    Image_url: str
    Cert_url: str
    Post_by: int
    Last_update: datetime


class PostUpdate(BaseModel):
    Id: Optional[int]
    Cat_id: Optional[int]
    Datetime: Optional[datetime]
    Post_type: Optional[int]
    Waste_type: Optional[int]
    Waste_code: Optional[str]
    Qty: Optional[float]
    Description: Optional[str]
    Detail: Optional[str]
    Image_url: Optional[str]
    Cert_url: Optional[str]
    Post_by: Optional[int]
    Last_update: Optional[datetime]
