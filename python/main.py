import os
import logging
import pathlib
import json
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "image"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.get("/items")
def get_item():
    if os.path.isfile("item.json"):
        with open("item.json") as file:
            item_dict = json.load(file)
    else:
        item_dict = {"item": []}
    
    return item_dict

@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...)):
    #item.jsonが既にあるとき
    if os.path.isfile("item.json"):
        with open("item.json") as file:
            item_dict = json.load(file)

    #item.jsonがないとき
    else:
        item_dict = {"item": []}
    
    #新しいitemの追加
    item_dict["item"].append({"name": name, "category": category})
    with open("item.json", "w") as file:
        json.dump(item_dict, file)
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

@app.get("/image/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image

    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
