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

"""
    Query Parameter and String Validations
    ######################################

    from typing import Optional
    from fastapi import FastAPI, Query

    app = FastAPI()
    @app.get("/items/")
    async def get_items(q: Optional[str] = None):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results

    1. Here q is not required query parameter type str with default value none.
    Eventhough q is optional, whenever it is provided we can add some validation, 
        e.g min length, max length.
    
    The code becomes:
    @app.get("/items/")
    async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results

    2. Now we can also add regex.
    The code becomes:
    @app.get("/items/")
    async def read_items(
        q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
    ):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results

    3. Query still optional but we can add default value.
    The code becomes:
    @app.get("/items/")
    async def read_items(q: str = Query("fixedquery", min_length=3)):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results
    
    4. Make it required by using python Ellipsis..
    @app.get("/items/")
    async def read_items(q: str = Query(..., min_length=3)):
        results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
        if q:
            results.update({"q": q})
        return results
    
    5. Query parameter list / multiple values
    EXPLICITLY use Query, otherwise it would be intepreted as a request body.
    The code becomes:
    @app.get("/items/")
    async def read_items(q: Optional[List[str]] = Query(None)):
        query_items = {"q": q}
        return query_items
    i.e
    http://localhost:8000/items/?q=foo&q=bar
    the the response to that URL would be:
    {
        "q": [
            "foo",
            "bar"
        ]
    }

    6. Query parameter list / multiple values with default
    
    @app.get("/items/")
    async def read_items(q: List[str] = Query(["foo", "bar"])):
        query_items = {"q": q}
        return query_items
    i.e
    http://localhost:8000/items/
    the the response to that URL would be:
    {
        "q": [
            "foo",
            "bar"
        ]
    }

"""