from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Amphur(BaseModel):
    Amphur_code: str
    Amphur_name: str
    Geo_id: int
    Province_id :int

    