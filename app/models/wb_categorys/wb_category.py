from pydantic import BaseModel
from datetime import date
from typing import Optional

class WbCategory(BaseModel):
    Name : str

class WbCategoryUpdate(BaseModel):
    Name : Optional[str]
