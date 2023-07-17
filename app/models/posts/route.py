
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.posts.post import Post, PostUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "posts"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Post)
def create_post(
    request: Request,
    post_data: Post
):
    post_data_dict = post_data.dict()
    result = collection.insert_one(post_data_dict)

    if result.acknowledged:
        created_post = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Post(**created_post)
    else:
        raise HTTPException(status_code=500, detail="Failed to create post")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_posts(
    request: Request
):
    posts = []
    for post in collection.find():
        id = str(post.pop('_id'))
        post["Id"] = id
        print("id : ",id)
        posts.append(post)
    return posts

@router.get("/{post_id}", response_model=Post)
def get_post(
    request: Request,
    post_id: str,

):
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return Post(**post)
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@router.post("/filters/", response_model=List[Post])
def get_post_by_filter(
    request: PostUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[Post]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    posts = []
    for post in cursor:
        posts.append(Post(id=str(post["_id"]), **post))

    return posts

@router.put("/{post_id}", response_model=Post)
def update_post(
    request: PostUpdate,
    post_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(post_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_post = collection.find_one({"_id": ObjectId(post_id)})
        return Post(**updated_post)
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}")
def delete_post(
    request: Request,
    post_id: str,
):

    result = collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")
