
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.blogs.blog import Blog
from app.models.blogs.blogItem import BlogItem
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "blogs"

# database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

#  -------------- BLOG Part --------------------------

@router.post("/", response_model=Blog)
def create_blog(
    request: Request,
    blog_data: Blog,
):

    blog_data_dict = blog_data.dict()
    result = collection.insert_one(blog_data_dict)

    if result.acknowledged:
        created_blog = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Blog(**created_blog)
    else:
        raise HTTPException(status_code=500, detail="Failed to create blog")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_blogs(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)
    blogs = []
    for blog in collection.find():
        id = str(blog.pop('_id'))
        blog["id"] = id
        print("id : ",id)
        blogs.append(blog)
    return blogs

@router.get("/{blog_id}", response_model=Blog)
def get_blog(
    request: Request,
    blog_id: str,
):
    blog = collection.find_one({"_id": ObjectId(blog_id)})
    if blog:
        return Blog(**blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.get("/filters/", response_model=List[Blog])
async def get_blog_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Blog]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    companies = []
    async for blog in cursor:
        companies.append(Blog(id=str(blog["_id"]), **blog))

    return companies

@router.put("/{blog_id}", response_model=Blog)
async def update_blog(
    request: Request,
    blog_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(blog_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_blog = collection.find_one({"_id": ObjectId(blog_id)})
        return Blog(**updated_blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


@router.delete("/{blog_id}")
def delete_blog(
    request: Request,
    blog_id: str,
):
    collection_name = "blogs"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    result = collection.delete_one({"_id": ObjectId(blog_id)})  # Convert blog_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Blog deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")


#  ------------------ BlogItem Part -----------------------


@router.post("/", response_model=BlogItem)
def create_blog(
    request: Request,
    blog_data: Blog,
):
    collection_name = "blog_items"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    
    blog_data_dict = blog_data.dict()
    result = collection.insert_one(blog_data_dict)

    if result.acknowledged:
        created_blog = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Blog(**created_blog)
    else:
        raise HTTPException(status_code=500, detail="Failed to create blog")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_blogs(
    request: Request,
):
    # host = htoken
    # collection = database_manager.get_collection(host)
    collection_name = "blog_items"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

    blogs = []
    for blog in collection.find():
        id = str(blog.pop('_id'))
        blog["id"] = id
        print("id : ",id)
        blogs.append(blog)
    return blogs

@router.get("/{item_id}", response_model=BlogItem)
def get_blog(
    request: Request,
    blog_id: str,
):
    collection_name = "blog_items"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    blog = collection.find_one({"_id": ObjectId(blog_id)})
    if blog:
        return Blog(**blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.get("/{blog_Item_id}", response_model=BlogItem)
def get_blog_Item(
    request: Request,
    blog_Item_id: str,
):


    blog_Item = collection.find_one({"_id": ObjectId(blog_Item_id)})
    if blog_Item:
        return BlogItem(**blog_Item)
    else:
        raise HTTPException(status_code=404, detail="BlogItem not found")

@router.get("/filters/", response_model=List[BlogItem])
async def get_blog_Item_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[BlogItem]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    blog_items = []
    async for blog_Item in cursor:
        blog_items.append(BlogItem(id=str(blog_Item["_id"]), **blog_Item))

    return blog_items

@router.put("/{item_id}", response_model=BlogItem)
def update_blog(
    request: Request,
    blog_id: str,
    blog_data,
    htoken: Optional[str] = Header(None)
):
    collection_name = "blog_items"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    result = collection.update_one({"_id": blog_id}, {"$set": blog_data.dict()})
    if result.modified_count == 1:
        updated_blog = collection.find_one({"_id": blog_id})
        return Blog(**updated_blog)
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/{item_id}")
def delete_blog(
    request: Request,
    blog_id: str,
):
    collection_name = "blog_items"
    collection = get_database_atlas("WEIS", atlas_uri)[collection_name]
    result = collection.delete_one({"_id": ObjectId(blog_id)})  # Convert blog_id to ObjectId
    if result.deleted_count == 1:
        return {"message": "Blog_Items deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Blog not found")

