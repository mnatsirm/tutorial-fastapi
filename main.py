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
        The code becomes:
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
        The code becomes:
            @app.get("/items/")
            async def read_items(q: List[str] = Query(["foo", "bar"])):
                query_items = {"q": q}
                return query_items
        i.e
            URL: http://localhost:8000/items/
        then the response to that URL would be:
            {
                "q": [
                    "foo",
                    "bar"
                ]
            }
    
    #######################################

    Path Parameters and Numeric Validations
    
    #######################################
    
    We can declare the same type of validations and metadata for path parameters with Path.
    1. Declare metadata
        the code:
            from fastapi import FastAPI, Path, Query
            from typing import Optional

            app = FastAPI()

            @app.get("/items/{item_id}")
            async def read_items(
                item_id: int = Path(..., title="The ID of the item to get"),
                q: Optional[str] = Query(None, alias="item-query"),
            ):
                results = {"item_id": item_id}
                if q:
                    results.update({"q": q})
                return results
        
        Because path parameter is always required as it has to be part of the path,
        thats why we declare with python ellipsis (e.g ...)
    
    2. Order the parameters.
        as far as i understand, FastAPI DOES NOT CARE about the order between Query, Path, etc..
        and theres also some python tricks to overcome "value with default before value that doesnt have default",
        BUT for readibility (to me atleast)
        let stick with this order: PATH -- QUERY -- ETC

    3. Number validations
        ge : greater than or equal
        le : less than or equal
        
        gt : greater than
        lt : less than
        
        the code:
            from fastapi import FastAPI, Path, Query

            app = FastAPI()

            @app.get("/items/{item_id}")
            async def read_items(
                item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
                size: float = Query(..., gt=0, lt=10.5)
                q: str = None,
            ):
                results = {"item_id": item_id}
                if q:
                    results.update({"q": q})
                return results
    
    ####################################

    Mix Path, Query, and Body parameters

    ####################################

    1. Starting point
    from fastapi import FastAPI, Path
    from typing import Optional
    from pydantic import BaseModel

    app = FastAPI()


    class Item(BaseModel):
        name: str
        description: Optional[str] = None
        price: float
        tax: Optional[float] = None


    @app.put("/items/{item_id}")
    async def update_item(
        *,
        item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
        q: Optional[str] = None,
        item: Optional[Item] = None,
    ):
        results = {"item_id": item_id}
        if q:
            results.update({"q": q})
        if item:
            results.update({"item": item})
        return results

"""