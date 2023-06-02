from fastapi import FastAPI

from app.models.users.route import router as users_router
from app.models.timers.route import router as timers_router
# from app.models.items.route import router as items_router
# from app.models.shops.route import router as shops_router
print("print from main")
# mongol part
app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(timers_router, prefix="/timers", tags=["timers"])

# app.include_router(items_router, prefix="/items", tags=["items"])
# app.include_router(shops_router, prefix="/shops", tags=["shops"])
