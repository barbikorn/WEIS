
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.wb_answers.wb_answer import WbAnswer, WbAnswerUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "wb_answers"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=WbAnswer)
def create_wb_answer(
    request: Request,
    wb_answer_data: WbAnswer
):
    wb_answer_data_dict = wb_answer_data.dict()
    result = collection.insert_one(wb_answer_data_dict)

    if result.acknowledged:
        created_wb_answer = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return WbAnswer(**created_wb_answer)
    else:
        raise HTTPException(status_code=500, detail="Failed to create wb_answer")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_wb_answers(
    request: Request
):
    wb_answers = []
    for wb_answer in collection.find():
        id = str(wb_answer.pop('_id'))
        wb_answer["Id"] = id
        print("id : ",id)
        wb_answers.append(wb_answer)
    return wb_answers

@router.get("/{wb_answer_id}", response_model=WbAnswer)
def get_wb_answer(
    request: Request,
    wb_answer_id: str,

):
    wb_answer = collection.find_one({"_id": ObjectId(wb_answer_id)})
    if wb_answer:
        return WbAnswer(**wb_answer)
    else:
        raise HTTPException(status_code=404, detail="Wb_answer not found")

@router.post("/filters/", response_model=List[WbAnswer])
def get_amphur_by_filter(
    request: WbAnswerUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[WbAnswer]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    amphurs = []
    for amphur in cursor:
        amphurs.append(WbAnswer(id=str(amphur["_id"]), **amphur))

    return amphurs

@router.put("/{wb_answer_id}", response_model=WbAnswer)
async def update_wb_answer(
    request: WbAnswerUpdate,
    wb_answer_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(wb_answer_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_wb_answer = collection.find_one({"_id": ObjectId(wb_answer_id)})
        return WbAnswer(**updated_wb_answer)
    else:
        raise HTTPException(status_code=404, detail="WbAnswer not found")

@router.delete("/{wb_answer_id}")
def delete_wb_answer(
    request: Request,
    wb_answer_id: str,
):

    result = collection.delete_one({"_id": ObjectId(wb_answer_id)})
    if result.deleted_count == 1:
        return {"message": "Wb_answer deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Wb_answer not found")
