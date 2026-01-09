# FastAPI Basics

## Table of Contents
- [Installation](#installation)
- [First Application](#first-application)
- [Path Parameters](#path-parameters)
- [Query Parameters](#query-parameters)
- [Request Body](#request-body)
- [Response Models](#response-models)
- [Status Codes](#status-codes)
- [Headers and Cookies](#headers-and-cookies)

## Installation

```bash
# Initialize project with uv
uv init my-api && cd my-api

# Full installation (recommended)
uv add "fastapi[standard]"

# Minimal installation
uv add fastapi uvicorn
```

The `[standard]` bundle includes:
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- `jinja2` - Templating
- `python-multipart` - Form data parsing

## First Application

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A sample API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Run development server:**
```bash
uv run fastapi dev main.py
```

**Run production server:**
```bash
uv run fastapi run main.py
# or
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Path Parameters

```python
# Basic path parameter
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# Multiple path parameters
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id}

# Path parameter with validation
from fastapi import Path

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(
        ...,
        title="Item ID",
        description="The ID of the item to retrieve",
        ge=1,  # Greater than or equal to 1
        le=1000  # Less than or equal to 1000
    )
):
    return {"item_id": item_id}

# Enum path parameters
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model": model_name, "message": f"Selected {model_name.value}"}

# Path containing slashes
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path}
```

## Query Parameters

```python
# Basic query parameters
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
# GET /items/?skip=20&limit=50

# Optional query parameters
@app.get("/items/")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    q: str | None = None
):
    results = {"skip": skip, "limit": limit}
    if q:
        results["q"] = q
    return results

# Required query parameters
@app.get("/items/")
async def list_items(q: str):  # No default = required
    return {"q": q}

# Query parameter validation
from fastapi import Query

@app.get("/items/")
async def list_items(
    q: str | None = Query(
        None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z]+$",
        title="Search query",
        description="Query string for searching items"
    )
):
    return {"q": q}

# List query parameters
@app.get("/items/")
async def list_items(tags: list[str] = Query([])):
    return {"tags": tags}
# GET /items/?tags=foo&tags=bar
```

## Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Basic request body
@app.post("/items/")
async def create_item(item: Item):
    return item

# Request body + path parameters
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

# Request body + path + query parameters
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: str | None = None
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result["q"] = q
    return result

# Multiple body parameters
from fastapi import Body

class User(BaseModel):
    username: str
    email: str

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(...)
):
    return {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
# Expects: {"item": {...}, "user": {...}, "importance": 5}

# Embed single body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    return {"item_id": item_id, "item": item}
# Expects: {"item": {"name": "...", ...}}
```

## Response Models

```python
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

# Filter response with response_model
@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # password is automatically excluded

# Multiple response models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}

# List response
@app.get("/users/", response_model=list[UserResponse])
async def list_users():
    return [{"id": 1, "username": "john", "email": "john@example.com"}]

# Exclude unset values
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item(item_id: int):
    return {"name": "Foo", "price": 50.2}  # Only returns set values
```

## Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None

# Common status codes
# 200 OK - Default for GET
# 201 Created - POST that creates resource
# 204 No Content - DELETE success
# 400 Bad Request - Client error
# 401 Unauthorized - Auth required
# 403 Forbidden - Auth failed
# 404 Not Found - Resource doesn't exist
# 422 Unprocessable Entity - Validation error
# 500 Internal Server Error - Server error
```

## Headers and Cookies

```python
from fastapi import Header, Cookie, Response

# Read headers
@app.get("/items/")
async def read_items(
    user_agent: str | None = Header(None),
    x_token: str | None = Header(None, alias="X-Token")
):
    return {"User-Agent": user_agent, "X-Token": x_token}

# Read cookies
@app.get("/items/")
async def read_items(session_id: str | None = Cookie(None)):
    return {"session_id": session_id}

# Set headers in response
@app.get("/items/")
async def read_items(response: Response):
    response.headers["X-Custom-Header"] = "custom-value"
    return {"message": "Hello"}

# Set cookies in response
@app.post("/login/")
async def login(response: Response):
    response.set_cookie(
        key="session",
        value="abc123",
        httponly=True,
        max_age=3600,
        secure=True
    )
    return {"message": "Logged in"}

# Delete cookie
@app.post("/logout/")
async def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "Logged out"}
```
