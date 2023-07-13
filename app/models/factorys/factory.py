from pydantic import BaseModel
from datetime import date

class Factory(BaseModel):
    No: int
    Fac_no: str
    Fac_name: str
    Address: str
    Tambon: str
    Amphur: str
    Province: str
    Phone: str
    Expire: date
