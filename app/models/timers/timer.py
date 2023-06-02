from pydantic import BaseModel
from typing import Optional

class Timer(BaseModel):
    id : Optional[str]
    time: int

    