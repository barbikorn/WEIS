from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

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


class WasteUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    volume: Optional[float]
    unit: Optional[str]
    state: Optional[str]
    source: Optional[str]
    period: Optional[str]
    period_volume: Optional[float]
    created_at: Optional[str]
    updated_at: Optional[str]
