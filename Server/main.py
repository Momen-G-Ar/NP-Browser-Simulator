from fastapi import FastAPI, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()

# item:
# name: str
# price: number
#
security = HTTPBasic()


class Item(BaseModel):
    name: str
    price: float


items = [
    {
        'name': 'ice-cream',
        'price': 23.3,
    }
]


@app.get("/items", status_code=status.HTTP_200_OK)
async def get_items(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'momin':
        return {"message": 'OK1', 'items': items, 'length': len(items)}
    return {"message": 'OK2', 'items': items, credentials: credentials, 'length': len(items)}


@app.post("/item")
async def create_item(item: Item, credentials: HTTPBasicCredentials = Depends(security)):
    items.append(item)
    if credentials.username == 'momin':
        print(1)
    return {'item': item}
