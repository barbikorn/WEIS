from pydantic import BaseModel, Field



class Generator(BaseModel):
    name: str
    address_number: str
    street: str
    district_id: str
    subdistrict_id: str
    province_id: str
    post_code: str
    created_at: str
    updated_at: str
