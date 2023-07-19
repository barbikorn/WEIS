
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.waste_codes.waste_code import WasteCode, WasteCodeUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "waste_codes"

collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=WasteCode)
def create_waste_code(
    request: Request,
    waste_code_data: WasteCode,

):
    waste_code_data_dict = waste_code_data.dict()
    result = collection.insert_one(waste_code_data_dict)

    if result.acknowledged:
        created_waste_code = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return WasteCode(**created_waste_code)
    else:
        raise HTTPException(status_code=500, detail="Failed to create waste_code")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_waste_codes(
    request: Request,
):
    waste_codes = []
    for waste_code in collection.find():
        id = str(waste_code.pop('_id'))
        waste_code["id"] = id
        print("id : ",id)
        waste_codes.append(waste_code)
    return waste_codes

@router.get("/{waste_code_id}", response_model=WasteCode)
def get_waste_code(
    waste_code_id: str,

):
    waste_code = collection.find_one({"_id": ObjectId(waste_code_id)})
    if waste_code:
        return WasteCode(**waste_code)
    else:
        raise HTTPException(status_code=404, detail="WasteCode not found")

@router.post("/filters/", response_model=List[WasteCode])
def get_waste_code_by_filter(
    request: WasteCodeUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[WasteCode]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    waste_codes = []
    for waste_code in cursor:
        waste_codes.append(WasteCode(id=str(waste_code["_id"]), **waste_code))

    return waste_codes


@router.put("/{waste_code_id}", response_model=WasteCode)
def update_waste_code(
    request: WasteCodeUpdate,
    waste_code_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(waste_code_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_waste_code = collection.find_one({"_id": ObjectId(waste_code_id)})
        return WasteCode(**updated_waste_code)
    else:
        raise HTTPException(status_code=404, detail="WasteCode not found")

@router.delete("/{waste_code_id}")
def delete_waste_code(
    request: Request,
    waste_code_id: str,
):
    result = collection.delete_one({"_id": ObjectId(waste_code_id)})
    if result.deleted_count == 1:
        return {"message": "WasteCode deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="WasteCode not found")
