
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict ,Any
from bson import ObjectId
from app.models.users.user import User,UserUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "users"
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]



@router.post("/", response_model=User)
def create_user(
    request: Request,
    user_data: User,

):
    user_data_dict = user_data.dict()
    result = collection.insert_one(user_data_dict)

    if result.acknowledged:
        created_user = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return User(**created_user)
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_users(
    request: Request,

):
    users = []
    for user in collection.find():
        user_id = str(user.pop('_id'))
        user["id"] = user_id
        users.append(User(**user))
    return users

@router.get("/{user_id}", response_model=User)
def get_user(
    request: Request,
    user_id: str,

):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/filters/", response_model=List[User])
async def get_user_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[User]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    users = []
    async for user in cursor:
        users.append(User(id=str(user["_id"]), **user))

    return users


@router.put("/{user_id}", response_model=User)
def update_user(
    request: UserUpdate,
    user_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_user = collection.find_one({"_id": ObjectId(user_id)})
        return User(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(
    request: Request,
    user_id: str,

):
    result = collection.delete_one({"_id": user_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
