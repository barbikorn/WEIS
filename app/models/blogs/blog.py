from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Blog(BaseModel):
    _id: ObjectId = Field(..., alias="_id")
    Amphur_code: str
    Amphur_name: str
    Geo_id: int
    Province_id :int

class Blog(BaseModel):
    _id: ObjectId = Field(..., alias="_id")
    Amphur_code: str
    Amphur_name: str
    Geo_id: int
    Province_id :int
