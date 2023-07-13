from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Emission_factor(BaseModel):
    Id : int
    Oil_type: str
    Car_type: str
    Drive_type: str
    Max_cap: str
    Loading: int
    Ef_Co2:int
    Ef_Ch4 :int
    Ef_N2o : int


    