from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel

class Waste(BaseModel):
    name: str
    type: str
    volume: float
    unit: str
    state: str
    source: str
    period: str
    period_volume: float
    created_at: str
    updated_at: str
