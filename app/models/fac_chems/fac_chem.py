from pydantic import BaseModel
from typing import Optional

class FacChem(BaseModel):
    Fac_id: str
    Chem_id: str


class FacChemUpdate(BaseModel):
    Fac_id: Optional[str]
    Chem_id: Optional[str]
