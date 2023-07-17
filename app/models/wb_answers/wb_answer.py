from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WbAnswer(BaseModel):
    Datetime: datetime
    Member_id: str
    Description: str
    Q_id: int

class WbAnswerUpdate(BaseModel):
    Datetime: Optional[datetime]
    Member_id: Optional[str]
    Description: Optional[str]
    Q_id: Optional[int]
