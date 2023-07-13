
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict
from bson import ObjectId
from app.models.waste_rules.waste_rule import Waste_rule
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "waste_rules"

collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Waste_rule)
def create_waste_rule(
    request: Request,
    waste_rule_data: Waste_rule,

):
    waste_rule_data_dict = waste_rule_data.dict()
    result = collection.insert_one(waste_rule_data_dict)

    if result.acknowledged:
        created_waste_rule = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Waste_rule(**created_waste_rule)
    else:
        raise HTTPException(status_code=500, detail="Failed to create waste_rule")

@router.get("/", response_model=List[Waste_rule])
def get_all_waste_rules(
    request: Request,
):
    waste_rules = []
    for waste_rule in collection.find():
        waste_rules.append(Waste_rule(**waste_rule))
    return waste_rules

@router.get("/{waste_rule_id}", response_model=Waste_rule)
def get_waste_rule(
    waste_rule_id: str,
    htoken: Optional[str] = Header(None)
):
    waste_rule = collection.find_one({"_id": ObjectId(waste_rule_id)})
    if waste_rule:
        return Waste_rule(**waste_rule)
    else:
        raise HTTPException(status_code=404, detail="Waste_rule not found")

@router.get("/filters/", response_model=List[Waste_rule])
async def get_waste_rule_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Waste_rule]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    waste_rules = []
    async for waste_rule in cursor:
        waste_rules.append(Waste_rule(id=str(waste_rule["_id"]), **waste_rule))

    return waste_rules


@router.put("/{waste_rule_id}", response_model=Waste_rule)
async def update_waste_rule(
    request: Request,
    waste_rule_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(waste_rule_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_waste_rule = collection.find_one({"_id": ObjectId(waste_rule_id)})
        return Waste_rule(**updated_waste_rule)
    else:
        raise HTTPException(status_code=404, detail="Waste_rule not found")

@router.delete("/{waste_rule_id}")
def delete_waste_rule(
    request: Request,
    waste_rule_id: str,
    htoken: Optional[str] = Header(None)
):

    result = collection.delete_one({"_id": ObjectId(waste_rule_id)})
    if result.deleted_count == 1:
        return {"message": "Waste_rule deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Waste_rule not found")
