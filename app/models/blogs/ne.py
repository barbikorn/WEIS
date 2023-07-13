@router.get("/{amphur_id}", response_model=BlogItem)
def get_amphur(
    request: Request,
    amphur_id: str,
):


    amphur = collection.find_one({"_id": ObjectId(amphur_id)})
    if amphur:
        return BlogItem(**amphur)
    else:
        raise HTTPException(status_code=404, detail="BlogItem not found")

@router.get("/filters/", response_model=List[BlogItem])
async def get_amphur_by_filter(
    request: Request,
    offset: int = 0,
    limit: int = 100
) -> List[BlogItem]:
    filter_params = await request.json()
    query = {}

    for field, value in filter_params.items():
        query[field] = value

    cursor = collection.find(query).skip(offset).limit(limit)
    companies = []
    async for amphur in cursor:
        companies.append(BlogItem(id=str(amphur["_id"]), **amphur))

    return companies