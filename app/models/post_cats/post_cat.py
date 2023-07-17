from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCat(BaseModel):
    Cat_id: str
    Datetime: datetime
    Post_type: str
    Waste_type: str
    Waste_code: str
    Qty: float
    Description: str
    Detail: str
    Image_url: str
    Cert_url: str
    Post_by: int
    Last_update: datetime


class PostCatUpdate(BaseModel):
    Cat_id: Optional[str]
    Datetime: Optional[datetime]
    Post_type: Optional[str]
    Waste_type: Optional[str]
    Waste_code: Optional[str]
    Qty: Optional[float]
    Description: Optional[str]
    Detail: Optional[str]
    Image_url: Optional[str]
    Cert_url: Optional[str]
    Post_by: Optional[int]
    Last_update: Optional[datetime]
