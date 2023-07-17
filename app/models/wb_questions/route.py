
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.wb_questions.wb_question import WbQuestion, WbQuestionUpdate
from app.database import get_database_atlas


router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
collection_name = "wb_questions"


collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=WbQuestion)
def create_wb_question(
    request: Request,
    wb_question_data: WbQuestion
):
    wb_question_data_dict = wb_question_data.dict()
    result = collection.insert_one(wb_question_data_dict)

    if result.acknowledged:
        created_wb_question = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return WbQuestion(**created_wb_question)
    else:
        raise HTTPException(status_code=500, detail="Failed to create wb_question")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_wb_questions(
    request: Request
):
    wb_questions = []
    for wb_question in collection.find():
        id = str(wb_question.pop('_id'))
        wb_question["Id"] = id
        print("id : ",id)
        wb_questions.append(wb_question)
    return wb_questions

@router.get("/{wb_question_id}", response_model=WbQuestion)
def get_wb_question(
    request: Request,
    wb_question_id: str,

):
    wb_question = collection.find_one({"_id": ObjectId(wb_question_id)})
    if wb_question:
        return WbQuestion(**wb_question)
    else:
        raise HTTPException(status_code=404, detail="Wb_question not found")

@router.post("/filters/", response_model=List[WbQuestion])
def get_wb_question_by_filter(
    request: WbQuestionUpdate,
    offset: int = 0,
    limit: int = 100
) -> List[WbQuestion]:
    filter_params = request.dict(exclude_unset=True)
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    wb_questions = []
    for wb_question in cursor:
        wb_questions.append(WbQuestion(id=str(wb_question["_id"]), **wb_question))

    return wb_questions

@router.get("/filter", response_model=List[WbQuestion])
def get_wb_questions_by_filter(
    request: Request,
    filter: Dict,
):
    wb_questions = []
    for wb_question in collection.find(filter):
        id = str(wb_question.pop('_id'))
        wb_question["id"] = id
        print("id : ",id)
        wb_questions.append(wb_question)
    return wb_questions

@router.put("/{wb_question_id}", response_model=WbQuestion)
def update_wb_question(
    request: WbQuestionUpdate,
    wb_question_id: str,
):
    updated_field = request.dict(exclude_unset=True)
    result = collection.update_one({"_id": ObjectId(wb_question_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_wb_question = collection.find_one({"_id": ObjectId(wb_question_id)})
        return WbQuestion(**updated_wb_question)
    else:
        raise HTTPException(status_code=404, detail="WbQuestion not found")

@router.delete("/{wb_question_id}")
def delete_wb_question(
    request: Request,
    wb_question_id: str,
):
    result = collection.delete_one({"_id": ObjectId(wb_question_id)})
    if result.deleted_count == 1:
        return {"message": "Wb_question deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Wb_question not found")
