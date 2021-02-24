from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def read_items():
    return [1,2,3,4,5]

@router.get("/{id}")
async def read_user_me(id:str = "0"):
    return {"id": id, "itemName":"ITEM{id}"}
