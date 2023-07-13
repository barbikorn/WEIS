
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.fac_chems.fac_chem import FacChem
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "fac_chems"

database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=FacChem)
def create_fac_chem(
    request: Request,
    fac_chem_data: FacChem
):
    fac_chem_data_dict = fac_chem_data.dict()
    result = collection.insert_one(fac_chem_data_dict)

    if result.acknowledged:
        created_fac_chem = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return FacChem(**created_fac_chem)
    else:
        raise HTTPException(status_code=500, detail="Failed to create fac_chem")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_fac_chems(
    request: Request
):
    fac_chems = []
    for fac_chem in collection.find():
        id = str(fac_chem.pop('_id'))
        fac_chem["Id"] = id
        print("id : ",id)
        fac_chems.append(fac_chem)
    return fac_chems

@router.get("/{fac_chem_id}", response_model=FacChem)
def get_fac_chem(
    request: Request,
    fac_chem_id: str,

):
    fac_chem = collection.find_one({"_id": ObjectId(fac_chem_id)})
    if fac_chem:
        return FacChem(**fac_chem)
    else:
        raise HTTPException(status_code=404, detail="Fac_chem not found")

@router.get("/filters/", response_model=List[FacChem])
async def get_fac_chem_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[FacChem]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    fac_chems = []
    async for fac_chem in cursor:
        fac_chems.append(FacChem(id=str(fac_chem["_id"]), **fac_chem))

    return fac_chems


@router.put("/{fac_chem_id}", response_model=FacChem)
async def update_fac_chem(
    request: Request,
    fac_chem_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(fac_chem_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_fac_chem = collection.find_one({"_id": ObjectId(fac_chem_id)})
        return FacChem(**updated_fac_chem)
    else:
        raise HTTPException(status_code=404, detail="FacChem not found")

@router.delete("/{fac_chem_id}")
def delete_fac_chem(
    request: Request,
    fac_chem_id: str,
):

    result = collection.delete_one({"_id": ObjectId(fac_chem_id)})
    if result.deleted_count == 1:
        return {"message": "Fac_chem deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Fac_chem not found")
