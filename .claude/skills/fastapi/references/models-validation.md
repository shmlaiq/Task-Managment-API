# Pydantic Models & Validation

## Table of Contents
- [Basic Models](#basic-models)
- [Field Validation](#field-validation)
- [Custom Validators](#custom-validators)
- [Nested Models](#nested-models)
- [Model Configuration](#model-configuration)
- [Common Patterns](#common-patterns)

## Basic Models

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 0.0
    tags: list[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["active", "inactive"] = "active"

# Usage
item = Item(name="Widget", price=9.99)
print(item.model_dump())  # Convert to dict
print(item.model_dump_json())  # Convert to JSON string
```

## Field Validation

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Annotated

class User(BaseModel):
    # String constraints
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, pattern=r"^(?=.*[A-Z])(?=.*\d)")

    # Numeric constraints
    age: int = Field(..., ge=0, le=150)
    score: float = Field(..., gt=0, lt=100)

    # URL validation
    website: HttpUrl | None = None

    # With examples for docs
    bio: str = Field(
        default="",
        max_length=500,
        examples=["Software developer from NYC"]
    )

# Using Annotated (modern approach)
from pydantic import Field
from typing import Annotated

Username = Annotated[str, Field(min_length=3, max_length=50)]
PositiveInt = Annotated[int, Field(gt=0)]

class User(BaseModel):
    username: Username
    points: PositiveInt
```

## Custom Validators

```python
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str

    # Field validator
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("must be alphanumeric")
        return v.lower()

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    # Model validator (access multiple fields)
    @model_validator(mode="after")
    def passwords_match(self) -> "User":
        if self.password != self.password_confirm:
            raise ValueError("passwords do not match")
        return self

# Before validator (transform before validation)
class Item(BaseModel):
    tags: list[str]

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",")]
        return v

# item = Item(tags="python, fastapi, api")  # Works!
```

## Nested Models

```python
from pydantic import BaseModel
from datetime import datetime

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Company(BaseModel):
    name: str
    address: Address

class User(BaseModel):
    id: int
    name: str
    email: str
    company: Company
    addresses: list[Address] = []
    created_at: datetime

# Example data
user_data = {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "company": {
        "name": "Acme Inc",
        "address": {
            "street": "123 Main St",
            "city": "NYC",
            "country": "USA",
            "zip_code": "10001"
        }
    },
    "created_at": "2024-01-15T10:30:00"
}
user = User(**user_data)
```

## Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        # Behavior
        strict=False,              # Allow type coercion
        validate_assignment=True,  # Validate on attribute assignment
        extra="forbid",           # Raise error on extra fields
        frozen=False,              # Allow mutation (True = immutable)

        # ORM mode (for SQLAlchemy)
        from_attributes=True,

        # JSON
        populate_by_name=True,     # Allow field name or alias

        # Examples for OpenAPI
        json_schema_extra={
            "examples": [
                {"username": "john_doe", "email": "john@example.com"}
            ]
        }
    )

    username: str
    email: str

# ORM mode example
from sqlalchemy.orm import Mapped

class UserDB:  # SQLAlchemy model
    id: int = 1
    username: str = "john"
    email: str = "john@example.com"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str

db_user = UserDB()
user_response = UserResponse.model_validate(db_user)
```

## Common Patterns

### Separate Create/Update/Response Models

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Base with shared fields
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None

# For creating users (includes password)
class UserCreate(UserBase):
    password: str

# For updating users (all optional)
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None

# For responses (includes id, excludes password)
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

# Usage in FastAPI
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Create user in DB...
    return db_user

@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    # Only update provided fields
    update_data = user.model_dump(exclude_unset=True)
    return updated_user
```

### Generic Response Wrapper

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: T | None = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

# Usage
@app.get("/users/{user_id}", response_model=Response[UserResponse])
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    return Response(data=user)

@app.get("/users/", response_model=PaginatedResponse[UserResponse])
async def list_users(page: int = 1, page_size: int = 10):
    users, total = get_users_paginated(page, page_size)
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### Computed Fields

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

### Alias for Different Field Names

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # Accept 'user_id' in JSON, but use 'id' in Python
    id: int = Field(..., alias="user_id")

    # Accept both 'userName' (JSON) and 'username' (Python)
    username: str = Field(..., alias="userName")

    model_config = ConfigDict(populate_by_name=True)

# Both work:
# User(user_id=1, userName="john")
# User(id=1, username="john")
```
