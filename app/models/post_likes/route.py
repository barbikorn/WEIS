
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.post_likes.post_like import PostLike, PostLikeUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "post_likes"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=PostLike)
def create_post_like(
    request: Request,
    post_like_data: PostLike
):
    post_like_data_dict = post_like_data.dict()
    result = collection.insert_one(post_like_data_dict)

    if result.acknowledged:
        created_post_like = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return PostLike(**created_post_like)
    else:
        raise HTTPException(status_code=500, detail="Failed to create post_like")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_post_likes(
    request: Request
):
    post_likes = []
    for post_like in collection.find():
        id = str(post_like.pop('_id'))
        post_like["Id"] = id
        print("id : ",id)
        post_likes.append(post_like)
    return post_likes

@router.get("/{post_like_id}", response_model=PostLike)
def get_post_like(
    request: Request,
    post_like_id: str,

):
    post_like = collection.find_one({"_id": ObjectId(post_like_id)})
    if post_like:
        return PostLike(**post_like)
    else:
        raise HTTPException(status_code=404, detail="Post_like not found")

@router.post("/filters/", response_model=List[PostLike])
def get_post_like_by_filter(
    request: PostLikeUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[PostLike]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    post_likes = []
    for post_like in cursor:
        post_likes.append(PostLike(id=str(post_like["_id"]), **post_like))

    return post_likes

@router.put("/{post_like_id}", response_model=PostLike)
def update_post_like(
    request: PostLikeUpdate,
    post_like_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(post_like_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_post_like = collection.find_one({"_id": ObjectId(post_like_id)})
        return PostLike(**updated_post_like)
    else:
        raise HTTPException(status_code=404, detail="PostLike not found")

@router.delete("/{post_like_id}")
def delete_post_like(
    request: Request,
    post_like_id: str,
):

    result = collection.delete_one({"_id": ObjectId(post_like_id)})
    if result.deleted_count == 1:
        return {"message": "Post_like deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post_like not found")
