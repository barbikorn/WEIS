
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.wb_categorys.wb_category import WbCategory, WbCategoryUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "wb_categorys"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=WbCategory)
def create_wb_category(
    request: Request,
    wb_category_data: WbCategory
):
    wb_category_data_dict = wb_category_data.dict()
    result = collection.insert_one(wb_category_data_dict)

    if result.acknowledged:
        created_wb_category = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return WbCategory(**created_wb_category)
    else:
        raise HTTPException(status_code=500, detail="Failed to create wb_category")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_wb_categorys(
    request: Request
):
    wb_categorys = []
    for wb_category in collection.find():
        id = str(wb_category.pop('_id'))
        wb_category["Id"] = id
        print("id : ",id)
        wb_categorys.append(wb_category)
    return wb_categorys

@router.get("/{wb_category_id}", response_model=WbCategory)
def get_wb_category(
    request: Request,
    wb_category_id: str,

):
    wb_category = collection.find_one({"_id": ObjectId(wb_category_id)})
    if wb_category:
        return WbCategory(**wb_category)
    else:
        raise HTTPException(status_code=404, detail="Wb_category not found")

@router.post("/filters/", response_model=List[WbCategory])
def get_wb_category_by_filter(
    request: WbCategoryUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[WbCategory]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    wb_categorys = []
    for wb_category in cursor:
        wb_categorys.append(WbCategory(id=str(wb_category["_id"]), **wb_category))

    return wb_categorys

@router.put("/{wb_category_id}", response_model=WbCategory)
def update_wb_category(
    request: WbCategoryUpdate,
    wb_category_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(wb_category_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_wb_category = collection.find_one({"_id": ObjectId(wb_category_id)})
        return WbCategory(**updated_wb_category)
    else:
        raise HTTPException(status_code=404, detail="WbCategory not found")

@router.delete("/{wb_category_id}")
def delete_wb_category(
    request: Request,
    wb_category_id: str,
):
    result = collection.delete_one({"_id": ObjectId(wb_category_id)})
    if result.deleted_count == 1:
        return {"message": "Wb_category deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Wb_category not found")
