
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.post_cats.post_cat import PostCat
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "post_cats"

database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=PostCat)
def create_post_cat(
    request: Request,
    post_cat_data: PostCat
):
    post_cat_data_dict = post_cat_data.dict()
    result = collection.insert_one(post_cat_data_dict)

    if result.acknowledged:
        created_post_cat = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return PostCat(**created_post_cat)
    else:
        raise HTTPException(status_code=500, detail="Failed to create post_cat")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_post_cats(
    request: Request
):
    post_cats = []
    for post_cat in collection.find():
        id = str(post_cat.pop('_id'))
        post_cat["Id"] = id
        print("id : ",id)
        post_cats.append(post_cat)
    return post_cats

@router.get("/{post_cat_id}", response_model=PostCat)
def get_post_cat(
    request: Request,
    post_cat_id: str,

):
    post_cat = collection.find_one({"_id": ObjectId(post_cat_id)})
    if post_cat:
        return PostCat(**post_cat)
    else:
        raise HTTPException(status_code=404, detail="Post_cat not found")

@router.get("/filters/", response_model=List[PostCat])
async def get_post_cat_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[PostCat]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    companies = []
    async for post_cat in cursor:
        companies.append(PostCat(id=str(post_cat["_id"]), **post_cat))

    return companies

@router.get("/filter", response_model=List[PostCat])
def get_post_cats_by_filter(
    request: Request,
    filter: Dict,
):
    post_cats = []
    for post_cat in collection.find(filter):
        id = str(post_cat.pop('_id'))
        post_cat["id"] = id
        print("id : ",id)
        post_cats.append(post_cat)
    return post_cats

@router.put("/{postCat_id}", response_model=PostCat)
async def update_postCat(
    request: Request,
    postCat_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(postCat_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_postCat = collection.find_one({"_id": ObjectId(postCat_id)})
        return PostCat(**updated_postCat)
    else:
        raise HTTPException(status_code=404, detail="PostCat not found")

@router.delete("/{post_cat_id}")
def delete_post_cat(
    request: Request,
    post_cat_id: str,
):

    result = collection.delete_one({"_id": ObjectId(post_cat_id)})
    if result.deleted_count == 1:
        return {"message": "Post_cat deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post_cat not found")
