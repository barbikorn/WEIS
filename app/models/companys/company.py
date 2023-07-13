from pydantic import BaseModel


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
