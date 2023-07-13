from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Waste_rule(BaseModel):
    Id : int
    Waste_rules: str
    Waste_kind: str
    Waste_name: str
    Waste_exam: str
    Waste_code: str
    Waste_usage:str
    Components:str
    Usate_rule:str
    Type_industry: str
    Product:str


    