
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.transporters.transporter import Transporter
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "transporters"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Transporter)
def create_transporter(
    request: Request,
    transporter_data: Transporter
):
    transporter_data_dict = transporter_data.dict()
    result = collection.insert_one(transporter_data_dict)

    if result.acknowledged:
        created_transporter = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Transporter(**created_transporter)
    else:
        raise HTTPException(status_code=500, detail="Failed to create transporter")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_transporters(
    request: Request
):
    transporters = []
    for transporter in collection.find():
        id = str(transporter.pop('_id'))
        transporter["Id"] = id
        print("id : ",id)
        transporters.append(transporter)
    return transporters

@router.get("/{transporter_id}", response_model=Transporter)
def get_transporter(
    request: Request,
    transporter_id: str,

):

    transporter = collection.find_one({"_id": transporter_id})
    if transporter:
        return Transporter(**transporter)
    else:
        raise HTTPException(status_code=404, detail="Transporter not found")

@router.post("/filters/", response_model=List[Transporter])
async def get_transporters_by_filter(
    request: Request,
    name: Optional[str] = None,
    email: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,

):
    query = {}
    if name:
        query["name"] = name
    if email:
        query["email"] = email

    transporters = []
    for transporter in collection.find(query).skip(offset).limit(limit):
        transporters.append(Transporter(id=str(transporter["_id"]), **transporter))
    return transporters

@router.get("/filter", response_model=List[Transporter])
def get_transporters_by_filter(
    request: Request,
    filter: Dict,

):

    transporters = []
    for transporter in collection.find(filter):
        id = str(transporter.pop('_id'))
        transporter["id"] = id
        print("id : ",id)
        transporters.append(transporter)
    return transporters

@router.put("/{transporter_id}", response_model=Transporter)
def update_transporter(
    request: Request,
    transporter_id: str,
    transporter_data,

):

    result = collection.update_one({"_id": transporter_id}, {"$set": transporter_data.dict()})
    if result.modified_count == 1:
        updated_transporter = collection.find_one({"_id": transporter_id})
        return Transporter(**updated_transporter)
    else:
        raise HTTPException(status_code=404, detail="Transporter not found")

@router.delete("/{transporter_id}")
def delete_transporter(
    request: Request,
    transporter_id: str,
):

    result = collection.delete_one({"_id": transporter_id})
    if result.deleted_count == 1:
        return {"message": "Transporter deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Transporter not found")
