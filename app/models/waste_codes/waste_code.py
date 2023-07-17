from pydantic import BaseModel
from typing import Optional

class WasteCode(BaseModel):
    Waste_group: str
    Name: str
    Code: str
    Danger: str


class WasteCodeUpdate(BaseModel):
    Waste_group: Optional[str]
    Name: Optional[str]
    Code: Optional[str]
    Danger: Optional[str]
