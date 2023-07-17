
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.emission_factors.emission_factor import EmissionFactor,EmissionFactorUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:93CXS054W26pEjL1@db-weis-8d1328f2.mongo.ondigitalocean.com/admin?authSource=admin&tls=true"
collection_name = "emission_factors"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]



@router.post("/", response_model=EmissionFactor)
def create_emission_factor(
    request: Request,
    emission_factor_data: EmissionFactor,
):
    emission_factor_data_dict = emission_factor_data.dict()
    result = collection.insert_one(emission_factor_data_dict)

    if result.acknowledged:
        created_emission_factor = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return EmissionFactor(**created_emission_factor)
    else:
        raise HTTPException(status_code=500, detail="Failed to create emission_factor")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_emission_factors(
    request: Request,
):
    emission_factors = []
    for emission_factor in collection.find():
        id = str(emission_factor.pop('_id'))
        emission_factor["id"] = id
        print("id : ",id)
        emission_factors.append(emission_factor)
    return emission_factors


@router.get("/{emission_factor_id}", response_model=EmissionFactor)
def get_emission_factor(
    request: Request,
    emission_factor_id: str,
):
    emission_factor = collection.find_one({"_id": ObjectId(emission_factor_id)})
    if emission_factor:
        return EmissionFactor(**emission_factor)
    else:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")

@router.post("/filters/", response_model=List[EmissionFactor])
def get_emission_factor_by_filter(
    request: EmissionFactorUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[EmissionFactor]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    emission_factors = []
    for emission_factor in cursor:
        emission_factors.append(EmissionFactor(id=str(emission_factor["_id"]), **emission_factor))

    return emission_factors


@router.put("/{emission_factor_id}", response_model=EmissionFactor)
async def update_emission_factor(
    request: EmissionFactorUpdate,
    emission_factor_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(emission_factor_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_emission_factor = collection.find_one({"_id": ObjectId(emission_factor_id)})
        return EmissionFactor(**updated_emission_factor)
    else:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")


@router.delete("/{emission_factor_id}")
def delete_emission_factor(
    request: Request,
    emission_factor_id: str,
):
    result = collection.delete_one({"_id": ObjectId(emission_factor_id)})
    if result.deleted_count == 1:
        return {"message": "EmissionFactor deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="EmissionFactor not found")
