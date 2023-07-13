
import json
import os
from fastapi import APIRouter, HTTPException, Request, Header
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.models.companys.company import Company
from app.database import get_database_atlas
from app.models.hosts.route import HostDatabaseManager

router = APIRouter()

atlas_uri = "mongodb+srv://doadmin:93CXS054W26pEjL1@db-weis-8d1328f2.mongo.ondigitalocean.com/admin?authSource=admin&tls=true"
collection_name = "companys"

database_manager = HostDatabaseManager(atlas_uri, collection_name)
collection = get_database_atlas("WEIS", atlas_uri)[collection_name]

@router.post("/", response_model=Company)
def create_company(
    request: Request,
    company_data: Company
):
    company_data_dict = company_data.dict()
    result = collection.insert_one(company_data_dict)

    if result.acknowledged:
        created_company = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return Company(**created_company)
    else:
        raise HTTPException(status_code=500, detail="Failed to create company")

@router.get("/", response_model=List[Dict[str, Any]])
def get_all_companys(
    request: Request
):
    companys = []
    for company in collection.find():
        id = str(company.pop('_id'))
        company["Id"] = id
        print("id : ",id)
        companys.append(company)
    return companys

@router.get("/{company_id}", response_model=Company)
def get_company(
    request: Request,
    company_id: str,
):
    company = collection.find_one({"_id": ObjectId(company_id)})
    if company:
        return Company(**company)
    else:
        raise HTTPException(status_code=404, detail="Company not found")

@router.get("/filters/", response_model=List[Company])
async def get_company_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Company]:
    filter_params = await request.json()
    query = {}
    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    companies = []
    async for company in cursor:
        companies.append(Company(id=str(company["_id"]), **company))

    return companies

@router.get("/filters/", response_model=List[Company])
async def get_company_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[Company]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    companys = []
    async for company in cursor:
        companys.append(Company(id=str(company["_id"]), **company))

    return companys


@router.put("/{company_id}", response_model=Company)
async def update_company(
    request: Request,
    company_id: str,
):
    updated_field = await request.json()
    result = collection.update_one({"_id": ObjectId(company_id)}, {"$set": updated_field})
    if result.modified_count == 1:
        updated_company = collection.find_one({"_id": ObjectId(company_id)})
        return Company(**updated_company)
    else:
        raise HTTPException(status_code=404, detail="Company not found")

@router.delete("/{company_id}")
def delete_company(
    request: Request,
    company_id: str,
):
    result = collection.delete_one({"_id": ObjectId(company_id)})
    if result.deleted_count == 1:
        return {"message": "Company deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Company not found")
