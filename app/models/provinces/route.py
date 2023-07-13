
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict
from bson import ObjectId
from app.models.provinces.province import Province
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "provinces"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

database_manager = HostDatabaseManager(atlas_uri, collection_name)

@router.post("/", response_model=Province)
def create_province(
    request: Request,
    province_data: Province,
):

    province_data_dict = province_data.dict()
    result = collection.insert_one(province_data_dict)

    if result.acknowledged:
        created_province = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Province(**created_province)
    else:
        raise HTTPException(status_code=500, detail="Failed to create province")

@router.get("/", response_model=List[Province])
def get_all_provinces(
    request: Request,
):

    provinces = []
    for province in collection.find():
        provinces.append(Province(**province))
    return provinces

@router.get("/{province_id}", response_model=Province)
def get_province(
    request: Request,
    province_id: str,
    htoken: Optional[str] = Header(None)
):
    host = htoken
    collection = database_manager.get_collection(host)

    province = collection.find_one({"_id": province_id})
    if province:
        return Province(**province)
    else:
        raise HTTPException(status_code=404, detail="Province not found")

@router.get("/filters/", response_model=List[Province])
async def get_province_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Province]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    provinces = []
    async for province in cursor:
        provinces.append(Province(id=str(province["_id"]), **province))

    return provinces


@router.put("/{province_id}", response_model=Province)
async def update_province(
    request: Request,
    province_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(province_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_province = collection.find_one({"_id": ObjectId(province_id)})
        return Province(**updated_province)
    else:
        raise HTTPException(status_code=404, detail="Province not found")

@router.delete("/{province_id}")
def delete_province(
    request: Request,
    province_id: str,
    htoken: Optional[str] = Header(None)
):
    host = htoken
    collection = database_manager.get_collection(host)

    result = collection.delete_one({"_id": province_id})
    if result.deleted_count == 1:
        return {"message": "Province deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Province not found")
