from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Amphur(BaseModel):
    Amphur_code: str
    Amphur_name: str
    Geo_id: int
    Province_id :int

class AmphurUpdate(BaseModel):
    Amphur_code: Optional[str]
    Amphur_name: Optional[str]
    Geo_id: Optional[int]
    Province_id :Optional[int]
    