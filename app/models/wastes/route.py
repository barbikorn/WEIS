
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.wastes.waste import Waste,WasteUpdate
from app.models.wastes.wasteItem import WasteItem
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"


#  -------------- BLOG Part --------------------------

@router.post("/", response_model=Waste)
def create_waste(
    request: Request,
    waste_data: Waste,
):
    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    
    waste_data_dict = waste_data.dict()
    result = collection.insert_one(waste_data_dict)

    if result.acknowledged:
        created_waste = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Waste(**created_waste)
    else:
        raise HTTPException(status_code=500, detail="Failed to create waste")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_wastes(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)
    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

    wastes = []
    for waste in collection.find():
        id = str(waste.pop('_id'))
        waste["id"] = id
        print("id : ",id)
        wastes.append(waste)
    return wastes

@router.get("/{waste_id}", response_model=Waste)
def get_waste(
    request: Request,
    waste_id: str,
):
    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    waste = collection.find_one({"_id": ObjectId(waste_id)})
    if waste:
        return Waste(**waste)
    else:
        raise HTTPException(status_code=404, detail="Waste not found")


@router.post("/filters/", response_model=List[Waste])
def get_amphur_by_filter(
    request: WasteUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[Waste]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    cursor = collection.find(query).skip(offset).limit(limit)
    amphurs = []
    for amphur in cursor:
        amphurs.append(Waste(id=str(amphur["_id"]), **amphur))

    return amphurs


@router.put("/{waste_id}", response_model=Waste)
def update_waste(
    request: WasteUpdate,
    waste_id: str,
):
    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(waste_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_waste = collection.find_one({"_id": ObjectId(waste_id)})
        return Waste(**updated_waste)
    else:
        raise HTTPException(status_code=404, detail="Waste not found")

@router.delete("/{waste_id}")
def delete_waste(
    request: Request,
    waste_id: str,
):
    collection_name = "wastes"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    result = collection.delete_one({"_id": ObjectId(waste_id)})  # Convert waste_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Waste deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Waste not found")


#  ------------------ WasteItem Part -----------------------


# @router.post("/", response_model=WasteItem)
# def create_waste(
#     request: Request,
#     waste_data: Waste,
# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    
#     waste_data_dict = waste_data.dict()
#     result = collection.insert_one(waste_data_dict)

#     if result.acknowledged:
#         created_waste = collection.find_one({"_id": ObjectId(result.inserted_id)})
#         return Waste(**created_waste)
#     else:
#         raise HTTPException(status_code=500, detail="Failed to create waste")

# @router.get("/", response_model=List[Dict[str, Any]])
# def get_all_wastes(
#     request: Request,
# ):
#     # host = htoken
#     # collection = database_manager.get_collection(host)
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

#     wastes = []
#     for waste in collection.find():
#         id = str(waste.pop('_id'))
#         waste["id"] = id
#         print("id : ",id)
#         wastes.append(waste)
#     return wastes

# @router.get("/{item_id}", response_model=WasteItem)
# def get_waste(
#     request: Request,
#     waste_id: str,
# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
#     waste = collection.find_one({"_id": ObjectId(waste_id)})
#     if waste:
#         return Waste(**waste)
#     else:
#         raise HTTPException(status_code=404, detail="Waste not found")

# @router.post("/filters/", response_model=List[WasteItem])
# async def get_wastes_by_filter(
#     request: Request,
#     name: Optional[str] = None,
#     email: Optional[str] = None,
#     offset: int = 0,
#     limit: int = 100,

# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
#     query = {}
#     if name:
#         query["name"] = name
#     if email:
#         query["email"] = email

#     wastes = []
#     for waste in collection.find(query).skip(offset).limit(limit):
#         wastes.append(Waste(id=str(waste["_id"]), **waste))
#     return wastes

# @router.get("/filter", response_model=List[WasteItem])
# def get_wastes_by_filter(
#     request: Request,
#     filter: Dict,

# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
#     wastes = []
#     for waste in collection.find(filter):
#         wastes.append(Waste(**waste))
#     return wastes

# @router.put("/{item_id}", response_model=WasteItem)
# def update_waste(
#     request: Request,
#     waste_id: str,
#     waste_data,

# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
#     result = collection.update_one({"_id": waste_id}, {"$set": waste_data.dict()})
#     if result.modified_count == 1:
#         updated_waste = collection.find_one({"_id": waste_id})
#         return Waste(**updated_waste)
#     else:
#         raise HTTPException(status_code=404, detail="Waste not found")

# @router.delete("/{item_id}")
# def delete_waste(
#     request: Request,
#     waste_id: str,
# ):
#     collection_name = "waste_items"
#     collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
#     result = collection.delete_one({"_id": ObjectId(waste_id)})  # Convert waste_id to ObjectId
#     if result.deleted_count == 1:
#         return {"message": "Waste_Items deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Waste not found")

