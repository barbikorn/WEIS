
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.receivers.receiver import Receiver
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "receivers"

# database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Receiver)
def create_receiver(
    request: Request,
    receiver_data: Receiver,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    receiver_data_dict = receiver_data.dict()
    result = collection.insert_one(receiver_data_dict)

    if result.acknowledged:
        created_receiver = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Receiver(**created_receiver)
    else:
        raise HTTPException(status_code=500, detail="Failed to create receiver")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_receivers(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    receivers = []
    for receiver in collection.find():
        id = str(receiver.pop('_id'))
        receiver["id"] = id
        print("id : ",id)
        receivers.append(receiver)
    return receivers

@router.get("/{receiver_id}", response_model=Receiver)
def get_receiver(
    request: Request,
    receiver_id: str,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    receiver = collection.find_one({"_id": ObjectId(receiver_id)})
    if receiver:
        return Receiver(**receiver)
    else:
        raise HTTPException(status_code=404, detail="Receiver not found")

@router.get("/filters/", response_model=List[Receiver])
async def get_receivers_by_filter(
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

    receivers = []
    for receiver in collection.find(query).skip(offset).limit(limit):
        receivers.append(Receiver(id=str(receiver["_id"]), **receiver))
    return receivers

@router.get("/filter", response_model=List[Receiver])
def get_receivers_by_filter(
    request: Request,
    filter: Dict,
    htoken: Optional[str] = Header(None)
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    receivers = []
    for receiver in collection.find(filter):
        receivers.append(Receiver(**receiver))
    return receivers

@router.put("/{receiver_id}", response_model=Receiver)
def update_receiver(
    request: Request,
    receiver_id: str,
    receiver_data,
    htoken: Optional[str] = Header(None)
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    result = collection.update_one({"_id": receiver_id}, {"$set": receiver_data.dict()})
    if result.modified_count == 1:
        updated_receiver = collection.find_one({"_id": receiver_id})
        return Receiver(**updated_receiver)
    else:
        raise HTTPException(status_code=404, detail="Receiver not found")

@router.delete("/{receiver_id}")
def delete_receiver(
    request: Request,
    receiver_id: str,
):
    # host = htoken
    # collection = database_manager.get_collection(host)

    result = collection.delete_one({"_id": ObjectId(receiver_id)})  # Convert receiver_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Receiver deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Receiver not found")
