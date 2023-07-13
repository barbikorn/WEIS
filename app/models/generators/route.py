
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.generators.generator import Generator
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "generators"

# database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Generator)
def create_generator(
    request: Request,
    generator_data: Generator,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    generator_data_dict = generator_data.dict()
    result = collection.insert_one(generator_data_dict)

    if result.acknowledged:
        created_generator = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Generator(**created_generator)
    else:
        raise HTTPException(status_code=500, detail="Failed to create generator")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_generators(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    generators = []
    for generator in collection.find():
        id = str(generator.pop('_id'))
        generator["id"] = id
        print("id : ",id)
        generators.append(generator)
    return generators

@router.get("/{generator_id}", response_model=Generator)
def get_generator(
    request: Request,
    generator_id: str,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    generator = collection.find_one({"_id": ObjectId(generator_id)})
    if generator:
        return Generator(**generator)
    else:
        raise HTTPException(status_code=404, detail="Generator not found")

@router.get("/filters/", response_model=List[Generator])
async def get_generators_by_filter(
    request: Request,
    name: Optional[str] = None,
    email: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    htoken: Optional[str] = Header(None)
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    query = {}
    if name:
        query["name"] = name
    if email:
        query["email"] = email

    generators = []
    for generator in collection.find(query).skip(offset).limit(limit):
        generators.append(Generator(id=str(generator["_id"]), **generator))
    return generators

@router.get("/filter", response_model=List[Generator])
def get_generators_by_filter(
    request: Request,
    filter: Dict,
    htoken: Optional[str] = Header(None)
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    generators = []
    for generator in collection.find(filter):
        generators.append(Generator(**generator))
    return generators

@router.put("/{generator_id}", response_model=Generator)
def update_generator(
    request: Request,
    generator_id: str,
    generator_data,
    htoken: Optional[str] = Header(None)
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    result = collection.update_one({"_id": generator_id}, {"$set": generator_data.dict()})
    if result.modified_count == 1:
        updated_generator = collection.find_one({"_id": generator_id})
        return Generator(**updated_generator)
    else:
        raise HTTPException(status_code=404, detail="Generator not found")

@router.delete("/{generator_id}")
def delete_generator(
    request: Request,
    generator_id: str,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    result = collection.delete_one({"_id": ObjectId(generator_id)})  # Convert generator_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Generator deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Generator not found")
