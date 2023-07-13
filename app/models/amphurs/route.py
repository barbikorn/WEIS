
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.amphurs.amphur import Amphur
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:93CXS054W26pEjL1@db-weis-8d1328f2.mongo.ondigitalocean.com/admin?authSource=admin&tls=true"
collection_name = "amphurs"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Amphur)
def create_amphur(
    request: Request,
    amphur_data: Amphur,
):

    amphur_data_dict = amphur_data.dict()
    result = collection.insert_one(amphur_data_dict)

    if result.acknowledged:
        created_amphur = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Amphur(**created_amphur)
    else:
        raise HTTPException(status_code=500, detail="Failed to create amphur")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_amphurs(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    amphurs = []
    for amphur in collection.find():
        id = str(amphur.pop('_id'))
        amphur["id"] = id
        print("id : ",id)
        amphurs.append(amphur)
    return amphurs

@router.get("/{amphur_id}", response_model=Amphur)
def get_amphur(
    request: Request,
    amphur_id: str,
):
    amphur = collection.find_one({"_id": ObjectId(amphur_id)})
    if amphur:
        return Amphur(**amphur)
    else:
        raise HTTPException(status_code=404, detail="Amphur not found")

@router.get("/filters/", response_model=List[Amphur])
async def get_amphur_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Amphur]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    amphurs = []
    async for amphur in cursor:
        amphurs.append(Amphur(id=str(amphur["_id"]), **amphur))

    return amphurs


@router.put("/{amphur_id}", response_model=Amphur)
async def update_amphur(
    request: Request,
    amphur_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(amphur_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_amphur = collection.find_one({"_id": ObjectId(amphur_id)})
        return Amphur(**updated_amphur)
    else:
        raise HTTPException(status_code=404, detail="Amphur not found")

@router.delete("/{amphur_id}")
def delete_amphur(
    request: Request,
    amphur_id: str,
):
    result = collection.delete_one({"_id": ObjectId(amphur_id)})  # Convert amphur_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Amphur deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Amphur not found")
