from pydantic import BaseModel
from datetime import date

class Chemical(BaseModel):
    No: int
    Name: str

