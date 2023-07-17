
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.waste_rules.waste_rule import WasteRule, WasteRuleUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "waste_rules"

collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=WasteRule)
def create_waste_rule(
    request: Request,
    waste_rule_data: WasteRule,

):
    waste_rule_data_dict = waste_rule_data.dict()
    result = collection.insert_one(waste_rule_data_dict)

    if result.acknowledged:
        created_waste_rule = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return WasteRule(**created_waste_rule)
    else:
        raise HTTPException(status_code=500, detail="Failed to create waste_rule")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_waste_rules(
    request: Request,
):
    waste_rules = []
    for waste_rule in collection.find():
        id = str(waste_rule.pop('_id'))
        waste_rule["id"] = id
        print("id : ",id)
        waste_rules.append(waste_rule)
    return waste_rules

@router.get("/{waste_rule_id}", response_model=WasteRule)
def get_waste_rule(
    waste_rule_id: str,

):
    waste_rule = collection.find_one({"_id": ObjectId(waste_rule_id)})
    if waste_rule:
        return WasteRule(**waste_rule)
    else:
        raise HTTPException(status_code=404, detail="WasteRule not found")

@router.post("/filters/", response_model=List[WasteRule])
def get_amphur_by_filter(
    request: WasteRuleUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[WasteRule]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    amphurs = []
    for amphur in cursor:
        amphurs.append(WasteRule(id=str(amphur["_id"]), **amphur))

    return amphurs


@router.put("/{waste_rule_id}", response_model=WasteRule)
def update_waste_rule(
    request: WasteRuleUpdate,
    waste_rule_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(waste_rule_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_waste_rule = collection.find_one({"_id": ObjectId(waste_rule_id)})
        return WasteRule(**updated_waste_rule)
    else:
        raise HTTPException(status_code=404, detail="WasteRule not found")

@router.delete("/{waste_rule_id}")
def delete_waste_rule(
    request: Request,
    waste_rule_id: str,

):

    result = collection.delete_one({"_id": ObjectId(waste_rule_id)})
    if result.deleted_count == 1:
        return {"message": "WasteRule deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="WasteRule not found")
