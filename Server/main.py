from fastapi import FastAPI, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse
from typing import List
import strings

app = FastAPI()

security = HTTPBasic()


items: List[dict] = [
    {
        'name': 'ice-cream',
        'price': 23.3,
    }
]

users = [
    {
        'username': 'momin',
        'password': '12345',
    },
    {
        'username': 'samir',
        'password': '1122334455',
    }
]


def check_credentials(credentials):
    return {'username': credentials.username,
            'password': credentials.password} in users


@app.get("/items", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_items(credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials):
        return strings.invalid_credentials_html
    html = strings.start_html + strings.our_items
    for index, _item in enumerate(items):
        html += strings.item.format(_item['name'], _item['price'])
    html += strings.end_html
    return html


@app.delete("/item", status_code=status.HTTP_204_NO_CONTENT, response_class=HTMLResponse)
async def delete_items(item: dict, credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials):
        return strings.invalid_credentials_html
    index_to_delete = None
    for i, item_ in enumerate(items):
        if item_['name'] == item['name']:
            index_to_delete = i
            break
    html_to_be_send = strings.start_html + strings.end_html
    # If the item is found, delete it using del
    if index_to_delete is not None:
        del items[index_to_delete]
    return html_to_be_send


@app.post("/item", status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def create_item(item: dict, credentials: HTTPBasicCredentials = Depends(security)):
    if not check_credentials(credentials):
        return strings.invalid_credentials_html
    items.append(item)
    html_to_be_send = strings.start_html + \
        strings.item_added_successfully + strings.end_html
    return html_to_be_send
