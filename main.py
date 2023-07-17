from fastapi import FastAPI

from app.models.users.route import router as users_router

from app.models.products.route import router as products_router
from app.models.provinces.route import router as provinces_router
from app.models.amphurs.route import router as amphurs_router
from app.models.districts.route import router as districts_router
from app.models.companys.route import router as companys_router
from app.models.members.route import router as members_router
from app.models.generators.route import router as generators_router
from app.models.receivers.route import router as receivers_router
from app.models.wastes.route import router as wastes_router
# from app.models.waste_manages.route import router as waste_manages_router

from app.models.factorys.route import router as factorys_router
from app.models.chemicals.route import router as chemicals_router
from app.models.fac_chems.route import router as fac_chems_router
from app.models.posts.route import router as posts_router
from app.models.post_cats.route import router as post_cats_router
from app.models.post_likes.route import router as post_likes_router
from app.models.wb_questions.route import router as wb_questions_router
from app.models.wb_answers.route import router as wb_answers_router
from app.models.wb_categorys.route import router as wb_categorys_router

from app.models.emission_factors.route import router as emission_factor_router
from app.models.waste_rules.route import router as waste_rule_router
from app.models.waste_codes.route import router as waste_codes_router

# from app.models.items.route import router as items_router
# from app.models.shops.route import router as shops_router
print("print from main")
# mongol part
app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
# app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(provinces_router, prefix="/provinces", tags=["provinces"])
app.include_router(amphurs_router, prefix="/amphurs", tags=["amphurs"])
app.include_router(districts_router, prefix="/districts", tags=["districts"])
app.include_router(companys_router, prefix="/companys", tags=["companys"])
app.include_router(emission_factor_router, prefix="/emission_factors", tags=["emission_factors"])
app.include_router(waste_rule_router, prefix="/waste_rules", tags=["waste_rules"])
app.include_router(waste_codes_router, prefix="/waste_codes", tags=["waste_codes"])
app.include_router(factorys_router, prefix="/factorys", tags=["factorys"])
app.include_router(chemicals_router, prefix="/chemicals", tags=["chemicals"])
app.include_router(fac_chems_router, prefix="/fac_chems", tags=["fac_chems"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(post_cats_router, prefix="/post_cats", tags=["post_cats"])
app.include_router(post_likes_router, prefix="/post_likes", tags=["post_likes"])
app.include_router(wb_questions_router, prefix="/wb_questions", tags=["wb_questions"])
app.include_router(wb_answers_router, prefix="/wb_answers", tags=["wb_answers"])
app.include_router(wb_categorys_router, prefix="/wb_categorys", tags=["wb_categorys"])


app.include_router(wastes_router, prefix="/wastes", tags=["wastes"])




# app.include_router(members_router, prefix="/members", tags=["members"])
# app.include_router(generators_router, prefix="/generators", tags=["generators"])
# app.include_router(receivers_router, prefix="/receivers", tags=["receivers"])
# app.include_router(items_router, prefix="/items", tags=["items"])
# app.include_router(shops_router, prefix="/shops", tags=["shops"])

# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)