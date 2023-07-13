from pydantic import BaseModel
from datetime import date

class FacChem(BaseModel):
    Fac_id : str
    Chem_id : str
    

