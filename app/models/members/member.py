from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Member(BaseModel):
    user_id: str
    company_id: str
    is_admin:bool
    created_at :str
    updated_at : str

    