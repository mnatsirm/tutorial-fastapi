from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    tax: Optional[float] = None
    description: Optional[str] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

@app.post("/items/{item_id}")
async def create_item(
    item_id: int, item: Item, notes: Optional[str] = None
):
    result = {"item_id": item_id, **item.dict()}
    if notes:
        result.update({"notes": notes})
    return result

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def get_item(
    item_id: str, is_fresh: bool, discount: int = 0, limit: Optional[int] = None
):
    item = {
        "item_id": item_id,
        "discount": discount,
        "is_fresh": is_fresh,
        "limit": limit
    }
    return item

@app.get("/users/me")
async def get_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }

    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }
    
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }
