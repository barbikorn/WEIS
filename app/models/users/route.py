from fastapi import APIRouter, HTTPException
from typing import List, Optional,Dict
from bson import ObjectId
from app.models.users.user import User
from app.database import get_database,get_database_atlas

# username = "admintest1"
# password = "admintest1"

router = APIRouter()
collection_name = "users"
# collection = get_database("oemplat", "localhost", 27017, username ,password)[collection_name]

#Atlas collection 
password="korn134Gcp"
# atlas_uri = "mongodb+srv://korngcp:{password}@cluster0.2u6ezly.mongodb.net/?retryWrites=true&w=majority"
# Mongo Ocean cluster
atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection = get_database_atlas("oemPlat", atlas_uri)[collection_name]
print("collection", collection)


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


# MockWebSocketResponse.return_value = AsyncIterator(range(5))

@router.post("/", response_model=User)
def create_user(user_data: User):
    user_data_dict = user_data.dict()
    result = collection.insert_one(user_data_dict)
    
    if result.acknowledged:
        created_user = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return User(**created_user)
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")

@router.get("/", response_model=List[User])
def get_all_users():
    users = []
    for user in collection.find():
        users.append(User(**user))
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str):
    user = collection.find_one({"_id": user_id})
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/filters/", response_model=List[User])
async def get_users_by_filter(
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

    users = []
    for user in collection.find(query).skip(offset).limit(limit):
        users.append(User(id=str(user["_id"]), **user))
    return users


@router.get("/filter", response_model=List[User])
def get_users_by_filter(filter: Dict):
    users = []
    for user in collection.find(filter):
        users.append(User(**user))
    return users


@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user_data):
    result = collection.update_one({"_id": user_id}, {"$set": user_data.dict()})
    if result.modified_count == 1:
        updated_user = collection.find_one({"_id": user_id})
        return User(**updated_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
def delete_user(user_id: str):
    result = collection.delete_one({"_id": user_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
