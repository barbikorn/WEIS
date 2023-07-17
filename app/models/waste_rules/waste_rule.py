from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WasteRule(BaseModel):
    Waste_rules: str
    Waste_kind: str
    Waste_name: str
    Waste_exam: str
    Waste_code: str
    Waste_usage: str
    Components: str
    Usate_rule: str
    Type_industry: str
    Product: str


class WasteRuleUpdate(BaseModel):
    Waste_rules: Optional[str]
    Waste_kind: Optional[str]
    Waste_name: Optional[str]
    Waste_exam: Optional[str]
    Waste_code: Optional[str]
    Waste_usage: Optional[str]
    Components: Optional[str]
    Usate_rule: Optional[str]
    Type_industry: Optional[str]
    Product: Optional[str]
