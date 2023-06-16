import json
import os
from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional, Dict
from bson import ObjectId
from app.models.users.user import User
from app.database import get_database_atlas

class HostDatabaseManager:
    def __init__(self, host_config_path: str, atlas_uri: str, collection_name: str):
        self.host_config_path = host_config_path
        self.atlas_uri = atlas_uri
        self.collection_name = collection_name
        self.host_config = self.load_host_config()

    def load_host_config(self) -> Dict[str, str]:
        with open(self.host_config_path) as f:
            host_config = json.load(f)
        return host_config

    def get_database_name(self, host: str) -> Optional[str]:
        host_config_entry = self.host_config.get(host)
        if host_config_entry:
            return host_config_entry.get("databasename")
        return None

    def get_collection(self, host: str):
        database_name = self.get_database_name(host)
        if database_name:
            return get_database_atlas(database_name, self.atlas_uri)[self.collection_name]
        raise HTTPException(status_code=404, detail="Database not found for the host")

router = APIRouter()
password = "xxxxxx"
atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "users"


current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
host_config_path = os.path.join(current_dir, "hostname.json")


database_manager = HostDatabaseManager(host_config_path, atlas_uri, collection_name)

@router.post("/", response_model=User)
def create_user(request: Request, user_data: User):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    user_data_dict = user_data.dict()
    result = collection.insert_one(user_data_dict)

    if result.acknowledged:
        created_user = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return User(**created_user)
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/", response_model=List[User])
def get_all_users(request: Request):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    users = []
    for user in collection.find():
        users.append(User(**user))
    return users

@router.get("/{user_id}", response_model=User)
def get_user(request: Request, user_id: str):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    user = collection.find_one({"_id": user_id})
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/filters/", response_model=List[User])
async def get_users_by_filter(
    request: Request,
    name: Optional[str] = None,
    email: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    query = {}
    if name:
        query["name"] = name
    if email:
        query["email"] = email

    users = []
    for user in collection.find(query).skip(offset).limit(limit):
        users.append(User(id=str(user["_id"]), **user))
    return users

@router.get("/filter", response_model=List[User])
def get_users_by_filter(request: Request, filter: Dict):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    users = []
    for user in collection.find(filter):
        users.append(User(**user))
    return users

@router.put("/{user_id}", response_model=User)
def update_user(request: Request, user_id: str, user_data):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    result = collection.update_one({"_id": user_id}, {"$set": user_data.dict()})
    if result.modified_count == 1:
        updated_user = collection.find_one({"_id": user_id})
        return User(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(request: Request, user_id: str):
    host = request.headers.get("host")
    collection = database_manager.get_collection(host)

    result = collection.delete_one({"_id": user_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
