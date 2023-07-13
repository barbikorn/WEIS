from pydantic import BaseModel
from datetime import datetime

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
