from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    Name: str
    Objective: str
    Waste_type: str
    Waste_name: str
    Waste_code: str
    Address: str
    District_id: str
    Amphur_id: str
    Province_id: str
    Phone: str
    Email: str
    Lat: float
    Lng: float
    Password: str
    Last_update: str


class CompanyUpdate(BaseModel):
    Name: Optional[str]
    Objective: Optional[str]
    Waste_type: Optional[str]
    Waste_name: Optional[str]
    Waste_code: Optional[str]
    Address: Optional[str]
    District_id: Optional[str]
    Amphur_id: Optional[str]
    Province_id: Optional[str]
    Phone: Optional[str]
    Email: Optional[str]
    Lat: Optional[float]
    Lng: Optional[float]
    Password: Optional[str]
    Last_update: Optional[str]
