
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict
from bson import ObjectId
from app.models.districts.district import District
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "districts"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

database_manager = HostDatabaseManager(atlas_uri, collection_name)

@router.post("/", response_model=District)
def create_district(
    request: Request,
    district_data: District,
    htoken: Optional[str] = Header(None)
):
    host = htoken
    collection = database_manager.get_collection(host)

    district_data_dict = district_data.dict()
    result = collection.insert_one(district_data_dict)

    if result.acknowledged:
        created_district = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return District(**created_district)
    else:
        raise HTTPException(status_code=500, detail="Failed to create district")

@router.get("/", response_model=List[District])
def get_all_districts(
    request: Request,
    htoken: Optional[str] = Header(None)
):
    host = htoken
    collection = database_manager.get_collection(host)

    districts = []
    for district in collection.find():
        districts.append(District(**district))
    return districts

@router.get("/{district_id}", response_model=District)
def get_district(
    request: Request,
    district_id: str,
):

    district = collection.find_one({"_id": district_id})
    if district:
        return District(**district)
    else:
        raise HTTPException(status_code=404, detail="District not found")

@router.get("/{district_id}", response_model=District)
def get_district(
    request: Request,
    district_id: str,
):


    district = collection.find_one({"_id": ObjectId(district_id)})
    if district:
        return District(**district)
    else:
        raise HTTPException(status_code=404, detail="District not found")

@router.get("/filters/", response_model=List[District])
async def get_district_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[District]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    districts = []
    async for district in cursor:
        districts.append(District(id=str(district["_id"]), **district))

    return districts

@router.put("/{district_id}", response_model=District)
async def update_district(
    request: Request,
    district_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(district_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_district = collection.find_one({"_id": ObjectId(district_id)})
        return District(**updated_district)
    else:
        raise HTTPException(status_code=404, detail="District not found")

@router.delete("/{district_id}")
def delete_district(
    request: Request,
    district_id: str,
    htoken: Optional[str] = Header(None)
):
    host = htoken
    collection = database_manager.get_collection(host)

    result = collection.delete_one({"_id": district_id})
    if result.deleted_count == 1:
        return {"message": "District deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="District not found")
