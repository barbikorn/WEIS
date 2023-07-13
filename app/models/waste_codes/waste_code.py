from pydantic import BaseModel

class WasteCode(BaseModel):
    Id: int
    Waste_group: str
    Name: str
    Code: str
    Danger: str