from pydantic import BaseModel
from datetime import date

class WbCategory(BaseModel):
    Name : str
