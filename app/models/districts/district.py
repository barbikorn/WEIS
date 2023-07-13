from pydantic import BaseModel
from typing import Optional

class District(BaseModel):
    District_id : int
    District_code: str
    District_name: str
    Amphur_id : int
    Province_id :int
    Geo_id : int

    