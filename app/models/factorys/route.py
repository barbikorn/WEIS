
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.factorys.factory import Factory, FactoryUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "factorys"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Factory)
def create_factory(
    request: Request,
    factory_data: Factory
):
    factory_data_dict = factory_data.dict()
    result = collection.insert_one(factory_data_dict)

    if result.acknowledged:
        created_factory = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Factory(**created_factory)
    else:
        raise HTTPException(status_code=500, detail="Failed to create factory")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_factorys(
    request: Request
):
    factorys = []
    for factory in collection.find():
        id = str(factory.pop('_id'))
        factory["Id"] = id
        print("id : ",id)
        factorys.append(factory)
    return factorys

@router.get("/{factory_id}", response_model=Factory)
def get_factory(
    request: Request,
    factory_id: str,

):
    factory = collection.find_one({"_id": ObjectId(factory_id)})
    if factory:
        return Factory(**factory)
    else:
        raise HTTPException(status_code=404, detail="Factory not found")

@router.post("/filters/", response_model=List[Factory])
def get_factory_by_filter(
    request: FactoryUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[Factory]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    factorys = []
    for factory in cursor:
        factorys.append(Factory(id=str(factory["_id"]), **factory))

    return factorys

@router.put("/{factory_id}", response_model=Factory)
def update_factory(
    request: FactoryUpdate,
    factory_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(factory_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_factory = collection.find_one({"_id": ObjectId(factory_id)})
        return Factory(**updated_factory)
    else:
        raise HTTPException(status_code=404, detail="Factory not found")

@router.delete("/{factory_id}")
def delete_factory(
    request: Request,
    factory_id: str,
):

    result = collection.delete_one({"_id": ObjectId(factory_id)})
    if result.deleted_count == 1:
        return {"message": "Factory deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Factory not found")
