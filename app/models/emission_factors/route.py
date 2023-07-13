
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict
from bson import ObjectId
from app.models.emission_factors.emission_factor import Emission_factor
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:93CXS054W26pEjL1@db-weis-8d1328f2.mongo.ondigitalocean.com/admin?authSource=admin&tls=true"
collection_name = "emission_factors"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

database_manager = HostDatabaseManager(atlas_uri, collection_name)

@router.post("/", response_model=Emission_factor)
def create_emission_factor(
    request: Request,
    emission_factor_data: Emission_factor,
):
    emission_factor_data_dict = emission_factor_data.dict()
    result = collection.insert_one(emission_factor_data_dict)

    if result.acknowledged:
        created_emission_factor = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Emission_factor(**created_emission_factor)
    else:
        raise HTTPException(status_code=500, detail="Failed to create emission_factor")

@router.get("/", response_model=List[Emission_factor])
def get_all_emission_factors(
    request: Request,
):
    emission_factors = []
    for emission_factor in collection.find():
        emission_factors.append(Emission_factor(**emission_factor))
    return emission_factors

@router.get("/{emission_factor_id}", response_model=Emission_factor)
def get_emission_factor(
    request: Request,
    emission_factor_id: str,
):

    emission_factor = collection.find_one({"_id": ObjectId(emission_factor_id)})
    if emission_factor:
        return Emission_factor(**emission_factor)
    else:
        raise HTTPException(status_code=404, detail="Emission_factor not found")

@router.get("/filters/", response_model=List[Emission_factor])
async def get_emission_factor_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Emission_factor]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    emission_factors = []
    async for emission_factor in cursor:
        emission_factors.append(Emission_factor(id=str(emission_factor["_id"]), **emission_factor))

    return emission_factors


@router.put("/{emission_factor_id}", response_model=Emission_factor)
async def update_emission_factor(
    request: Request,
    emission_factor_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(emission_factor_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_emission_factor = collection.find_one({"_id": ObjectId(emission_factor_id)})
        return Emission_factor(**updated_emission_factor)
    else:
        raise HTTPException(status_code=404, detail="Emission_factor not found")


@router.delete("/{emission_factor_id}")
def delete_emission_factor(
    request: Request,
    emission_factor_id: str,
):
    result = collection.delete_one({"_id": emission_factor_id})
    if result.deleted_count == 1:
        return {"message": "Emission_factor deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Emission_factor not found")
