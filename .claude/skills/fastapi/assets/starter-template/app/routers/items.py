from fastapi import APIRouter, HTTPException
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

# In-memory storage (replace with database)
items_db: dict[int, Item] = {}
item_id_counter = 0


@router.get("/", response_model=list[Item])
async def list_items(skip: int = 0, limit: int = 100):
    return list(items_db.values())[skip : skip + limit]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    global item_id_counter
    item_id_counter += 1
    db_item = Item(id=item_id_counter, **item.model_dump())
    items_db[item_id_counter] = db_item
    return db_item


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    items_db[item_id] = updated_item
    return updated_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
