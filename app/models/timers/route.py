from fastapi import APIRouter, HTTPException
from typing import List, Optional,Dict
from bson import ObjectId
from app.models.timers.timer import Timer
from app.database import get_database,get_database_atlas
from typing import Dict, Any ,List

# timername = "admintest1"
# password = "admintest1"

router = APIRouter()
collection_name = "timers"
# collection = get_database("oemplat", "localhost", 27017, timername ,password)[collection_name]

#Atlas collection 
password="korn134Gcp"
# atlas_uri = "mongodb+srv://korngcp:{password}@cluster0.2u6ezly.mongodb.net/?retryWrites=true&w=majority"
# Mongo Ocean cluster
atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection = get_database_atlas("oemPlat", atlas_uri)[collection_name]

print("collection", collection)
# if collection is None:
#     # Handle the error condition here
#     print("Error: Unable to access the collection due to connection issues.")
# else:
#     # Perform operations on the collection
#     # ...
#     print("collection", collection)


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



@router.get("/allId", response_model=List[Dict[str, Any]])
def get_all_timer_data():
    timer_data = []
    for timer in collection.find():
        timer_id = str(timer.pop('_id'))
        timer["id"] = timer_id
        timer_data.append(timer)
    return timer_data



# INCREASE?DECREASE TIME 
##########
@router.post("/{timer_id}/increaseTime", response_model=Timer)
def increase_time(timer_id: str):
    timer = collection.find_one({"_id": ObjectId(timer_id)})

    if timer:
        updated_time = timer["time"] + 1
        collection.update_one({"_id": ObjectId(timer_id)}, {"$set": {"time": updated_time}})
        timer["time"] = updated_time
        return timer
    else:
        raise HTTPException(status_code=404, detail="Timer not found")


@router.post("/{timer_id}/decreaseTime", response_model=Timer)
def decrease_time(timer_id: str):
    timer = collection.find_one({"_id": ObjectId(timer_id)})

    if timer:
        updated_time = timer["time"] - 1
        collection.update_one({"_id": ObjectId(timer_id)}, {"$set": {"time": updated_time}})
        timer["time"] = updated_time
        return timer
    else:
        raise HTTPException(status_code=404, detail="Timer not found")
# MockWebSocketResponse.return_value = AsyncIterator(range(5))



# CRUD
#############
@router.post("/", response_model=Timer)
def create_timer(timer_data: Timer):
    timer_data_dict = timer_data.dict()
    result = collection.insert_one(timer_data_dict)

    if result.acknowledged:
        created_timer_id = str(result.inserted_id)
        created_timer = {"id": created_timer_id, "time": timer_data_dict["time"]}
        return Timer(**created_timer)
    else:
        raise HTTPException(status_code=500, detail="Failed to create timer")


@router.get("/", response_model=List[Timer])
def get_all_timers():
    timers = []
    for timer_data in collection.find():
        timer = Timer(**timer_data)  # Instantiate a Timer object using the dictionary values
        timers.append(timer)
    return timers


@router.get("/{timer_id}", response_model=Timer)
def get_timer(timer_id: str):
    timer = collection.find_one({"_id": ObjectId(timer_id)})  # Convert timer_id to ObjectId
    if timer:
        return Timer(**timer)
    else:
        raise HTTPException(status_code=404, detail="Timer not found")

@router.get("/filters/", response_model=List[Timer])
async def get_timers_by_filter(
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

    timers = []
    for timer in collection.find(query).skip(offset).limit(limit):
        timers.append(timer(id=str(timer["_id"]), **timer))
    return timers


@router.get("/filter", response_model=List[Timer])
def get_timers_by_filter(filter: Dict):
    timers = []
    for timer in collection.find(filter):
        timers.append(timer(**timer))
    return timers


@router.put("/{timer_id}", response_model=Timer)
def update_timer(timer_id: str, timer_data):
    result = collection.update_one({"_id": timer_id}, {"$set": timer_data.dict()})
    if result.modified_count == 1:
        updated_timer = collection.find_one({"_id": timer_id})
        return Timer(**updated_timer)
    else:
        raise HTTPException(status_code=404, detail="timer not found")


@router.delete("/{timer_id}")
def delete_timer(timer_id: str):
    result = collection.delete_one({"_id": timer_id})
    if result.deleted_count == 1:
        return {"message": "timer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="timer not found")
