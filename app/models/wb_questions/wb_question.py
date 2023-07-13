from pydantic import BaseModel
from datetime import datetime

class WbQuestion(BaseModel):
    Title: str
    Description: str
    Hits: int
    Datetime: datetime
    Member_id: str
    Cat_id: str
