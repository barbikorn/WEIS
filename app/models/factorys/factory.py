from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Factory(BaseModel):
    No: int
    Fac_no: str
    Fac_name: str
    Address: str
    Tambon: str
    Amphur: str
    Province: str
    Phone: str
    Expire: datetime


class FactoryUpdate(BaseModel):
    No: Optional[int]
    Fac_no: Optional[str]
    Fac_name: Optional[str]
    Address: Optional[str]
    Tambon: Optional[str]
    Amphur: Optional[str]
    Province: Optional[str]
    Phone: Optional[str]
    Expire: Optional[datetime]
