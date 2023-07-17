from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmissionFactor(BaseModel):
    Oil_type: str
    Car_type: str
    Drive_type: str
    Max_cap: str
    Loading: int
    Ef_Co2: int
    Ef_Ch4: int
    Ef_N2o: int


class EmissionFactorUpdate(BaseModel):
    Oil_type: Optional[str]
    Car_type: Optional[str]
    Drive_type: Optional[str]
    Max_cap: Optional[str]
    Loading: Optional[int]
    Ef_Co2: Optional[int]
    Ef_Ch4: Optional[int]
    Ef_N2o: Optional[int]
