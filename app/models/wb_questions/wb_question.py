from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WbQuestion(BaseModel):
    Title: str
    Description: str
    Hits: int
    Datetime: datetime
    Member_id: str
    Cat_id: str


class WbQuestionUpdate(BaseModel):
    Title: Optional[str]
    Description: Optional[str]
    Hits: Optional[int]
    Datetime: Optional[datetime]
    Member_id: Optional[str]
    Cat_id: Optional[str]
