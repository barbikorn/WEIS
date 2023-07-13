from pydantic import BaseModel
from typing import Optional

class Province(BaseModel):
    Province_id : int
    Province_code: str
    Province_name: str
    Geo_id: str

    