
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.members.member import Member
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "members"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Member)
def create_member(
    request: Request,
    member_data: Member
):
    member_data_dict = member_data.dict()
    result = collection.insert_one(member_data_dict)

    if result.acknowledged:
        created_member = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Member(**created_member)
    else:
        raise HTTPException(status_code=500, detail="Failed to create member")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_members(
    request: Request
):
    members = []
    for member in collection.find():
        id = str(member.pop('_id'))
        member["Id"] = id
        print("id : ",id)
        members.append(member)
    return members

@router.get("/{member_id}", response_model=Member)
def get_member(
    request: Request,
    member_id: str,

):

    member = collection.find_one({"_id": member_id})
    if member:
        return Member(**member)
    else:
        raise HTTPException(status_code=404, detail="Member not found")

@router.post("/filters/", response_model=List[Member])
async def get_members_by_filter(
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

    members = []
    for member in collection.find(query).skip(offset).limit(limit):
        members.append(Member(id=str(member["_id"]), **member))
    return members

@router.get("/filter", response_model=List[Member])
def get_members_by_filter(
    request: Request,
    filter: Dict,

):


    members = []
    for member in collection.find(filter):
        id = str(member.pop('_id'))
        member["id"] = id
        print("id : ",id)
        members.append(member)
    return members

@router.put("/{member_id}", response_model=Member)
def update_member(
    request: Request,
    member_id: str,
    member_data,

):


    result = collection.update_one({"_id": member_id}, {"$set": member_data.dict()})
    if result.modified_count == 1:
        updated_member = collection.find_one({"_id": member_id})
        return Member(**updated_member)
    else:
        raise HTTPException(status_code=404, detail="Member not found")

@router.delete("/{member_id}")
def delete_member(
    request: Request,
    member_id: str,

):


    result = collection.delete_one({"_id": member_id})
    if result.deleted_count == 1:
        return {"message": "Member deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Member not found")
