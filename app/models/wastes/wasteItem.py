from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class WasteItem(BaseModel):
    name: str
    value: str
    type: str
    waste_id: str
    created_at: str
    updated_at: str
