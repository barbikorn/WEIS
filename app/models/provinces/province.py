from pydantic import BaseModel
from typing import Optional

class Province(BaseModel):
    Province_code: str
    Province_name: str
    Geo_id: str


class ProvinceUpdate(BaseModel):
    Province_code: Optional[str]
    Province_name: Optional[str]
    Geo_id: Optional[str]
