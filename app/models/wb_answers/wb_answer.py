from pydantic import BaseModel
from datetime import datetime

class WbAnswer(BaseModel):
    Datetime: datetime
    Member_id: str
    Description: str
    Q_id: int
