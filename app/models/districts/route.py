
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.districts.district import District , DistrictUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "districts"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]



@router.post("/", response_model=District)
def create_district(
    request: Request,
    district_data: District,

):
    district_data_dict = district_data.dict()
    result = collection.insert_one(district_data_dict)

    if result.acknowledged:
        created_district = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return District(**created_district)
    else:
        raise HTTPException(status_code=500, detail="Failed to create district")


@router.get("/", response_model=List[Dict[str, Any]])
def get_all_districts(
    request: Request,
):
    districts = []
    for district in collection.find():
        id = str(district.pop('_id'))
        district["id"] = id
        print("id : ",id)
        districts.append(district)
    return districts

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

@router.post("/filters/", response_model=List[District])
def get_district_by_filter(
    request: DistrictUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[District]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    districts = []
    for district in cursor:
        districts.append(District(id=str(district["_id"]), **district))

    return districts

@router.put("/{district_id}", response_model=District)
async def update_district(
    request: DistrictUpdate,
    district_id: str,
):
    updated_field = request.dict(exclude_unset=True)
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
):
    result = collection.delete_one({"_id": ObjectId(district_id)})
    if result.deleted_count == 1:
        return {"message": "District deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="District not found")
