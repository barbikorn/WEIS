
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.chemicals.chemical import Chemical,ChemicalUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "chemicals"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Chemical)
def create_chemical(
    request: Request,
    chemical_data: Chemical
):
    chemical_data_dict = chemical_data.dict()
    result = collection.insert_one(chemical_data_dict)

    if result.acknowledged:
        created_chemical = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Chemical(**created_chemical)
    else:
        raise HTTPException(status_code=500, detail="Failed to create chemical")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_chemicals(
    request: Request
):
    chemicals = []
    for chemical in collection.find():
        id = str(chemical.pop('_id'))
        chemical["Id"] = id
        print("id : ",id)
        chemicals.append(chemical)
    return chemicals

@router.get("/{chemical_id}", response_model=Chemical)
def get_chemical(
    request: Request,
    chemical_id: str,

):
    chemical = collection.find_one({"_id": ObjectId(chemical_id)})
    if chemical:
        return Chemical(**chemical)
    else:
        raise HTTPException(status_code=404, detail="Chemical not found")

@router.post("/filters/", response_model=List[Chemical])
def get_chemical_by_filter(
    request: ChemicalUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[Chemical]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    chemicals = []
    for chemical in cursor:
        chemicals.append(Chemical(id=str(chemical["_id"]), **chemical))

    return chemicals

@router.put("/{chemical_id}", response_model=Chemical)
def update_chemical(
    request: ChemicalUpdate,
    chemical_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(chemical_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_chemical = collection.find_one({"_id": ObjectId(chemical_id)})
        return Chemical(**updated_chemical)
    else:
        raise HTTPException(status_code=404, detail="Chemical not found")

@router.delete("/{chemical_id}")
def delete_chemical(
    request: Request,
    chemical_id: str,
):
    result = collection.delete_one({"_id": ObjectId(chemical_id)})
    if result.deleted_count == 1:
        return {"message": "Chemical deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chemical not found")
