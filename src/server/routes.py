from fastapi import FastAPI, APIRouter, Body, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from typing import Optional
from pydantic import BaseModel
import shutil
from typing import List
from PIL import Image
import PIL
import uvicorn

from src.database import (
    car_add,
    single_car_retrieve,
    all_cars_retrieve,
    car_update,
    car_delete,
)
from src.models.car_model import CarSchema, UpdateCarModel
from src.models.response_models import ErrorResponseModel, ResponseModel
from src.models.client_model import ClientSchema

router = APIRouter()
    
@router.get("/sample")
async def sendInfo():
    return {
        "CarSample":{
            "owner": "Mauricio",
            "manufacturer": "Ferrari",
            "year": 2
        }
    }

@router.post("/client/")
async def create_client(client: ClientSchema):
    return client

# create
@router.post("/post", response_description="A car has been created")
async def add_new_car(car: CarSchema = Body(...)):
    car = jsonable_encoder(car)
    new_car = await car_add(car)
    return ResponseModel(new_car, "Car created successfully.")

#retrieve all
@router.get("/get", response_description="All car collections")
async def get_all_cars():
    cars = await retrieve_all_cars()
    if cars:
        return ResponseModel(cars, "All cars have been retrieved")
    return ResponseModel(cars, "Empty list returned")

#get one
@router.get("/get/{id}", response_description="Single Car retrieve")
async def get_a_car(id):
    car = await retrieve_single_car(id)
    if car:
        return ResponseModel(car, "Car READ")
    return ErrorResponseModel("An error occurred.", 404, "Car is gone")

#update
@router.put("/put/{id}")
async def car_updater(id: str, req: UpdateCarModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_car = await update_car(id, req)
    if updated_car:
        return ResponseModel(
            "Car with register {} has been updated".format(id),
            'this is the message ?'
        )
    return ErrorResponseModel("An error occurred", 404, ":(")

#delete
@router.delete("/del/{id}", response_description="Car deleted")
async def car_remover(id: str):
    car_to_be_deleted = await delete_car(id)
    if car_to_be_deleted:
        return ResponseModel("Car with register {} removed".format(id), "Deleted")
    return ErrorResponseModel("An error occurred", 404, "This is a real 404")

@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        with open("receive.png", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return HTMLResponse(content=content)

@router.get("/home", response_class=HTMLResponse)
async def main():
    #return HTMLResponse(content=content)
    return FileResponse ("src/templates/upload_image.html")

@router.get("/last_pic")
async def stream():
    path = "receive.png"
    file_like = open(path, mode="rb")
    return StreamingResponse(file_like, media_type="image/png")
