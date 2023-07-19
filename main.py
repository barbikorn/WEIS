from fastapi import FastAPI
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Depends, status
from typing import List, Optional, Dict ,Any, Union
from bson import ObjectId
from app.models.users.user import User,UserUpdate,UserCreate, Token, TokenData
from app.database import get_database_atlas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing_extensions import Annotated
from fastapi.openapi.utils import get_openapi

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



atlas_uri = "mongodb+srv://doadmin:AU97Jfe026gE415o@db-mongodb-kornxecobz-8ade0110.mongo.ondigitalocean.com/admin?tls=true&authSource=admin"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user( email: str, password: str):
    collection = get_database_atlas("WEIS", atlas_uri)["users"]
    user = collection.find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    collection = get_database_atlas("WEIS", atlas_uri)["users"]
    user = collection.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    user_data_dict = user_data.dict()
    user_data_dict["password"] = get_password_hash(user_data_dict["password"])
    collection = get_database_atlas("WEIS", atlas_uri)["users"]
    result = collection.insert_one(user_data_dict)
    
    if result.acknowledged:
        created_user = collection.find_one({"_id": ObjectId(result.inserted_id)})
        return User(**created_user)
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user




# app.include_router(members_router, prefix="/members", tags=["members"])
# app.include_router(generators_router, prefix="/generators", tags=["generators"])
# app.include_router(receivers_router, prefix="/receivers", tags=["receivers"])
# app.include_router(items_router, prefix="/items", tags=["items"])
# app.include_router(shops_router, prefix="/shops", tags=["shops"])






# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)