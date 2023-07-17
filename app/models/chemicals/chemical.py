from pydantic import BaseModel
from typing import Optional

class Chemical(BaseModel):
    No: int
    Name: str

class ChemicalUpdate(BaseModel):
    No: Optional[int]
    Name: Optional[str]