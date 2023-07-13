from pydantic import BaseModel
from datetime import datetime

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
