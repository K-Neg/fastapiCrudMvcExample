from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from src.database import (
    add_car,
    retrieve_single_car,
    retrieve_all_cars,
    update_car,
    delete_car,
)
from src.car_model import (
    ErrorResponseModel,
    ResponseModel,
    CarSchema,
    UpdateCarModel,
)

router = APIRouter()

html_content = """
    <html>
        <head>
            <title>RouterTestPage</title>
        </head>
        <body>
            <h1>Hello World Router</h1>
        </body>
    </html>
    """


@router.get("/info")
async def sendInfo():
    return {
        "CarSample":{
            "owner": "Mauricio",
            "manufacturer": "Ferrari",
            "year": 2
        }
    }

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class Carro(BaseModel):
    owner: str
    manufacturer: Optional[str] = None
    year: Optional[int]
    
@router.post("/items/")
async def create_item(item: Item):
    return item

# create
@router.post("/post", response_description="A car has been created")
#async def add_car_ROUTE(car: Carro):
async def add_car_ROUTE(car: CarSchema = Body(...)):
    print('pre Enc')
    car = jsonable_encoder(car)
    print('pos enc')
    new_car = await add_car(car)
    print("after new car")
    return ResponseModel(new_car, "Car created successfully.")


@router.get("/get", response_description="All car collections")
async def get_all_cars():
    cars = await retrieve_all_cars()
    if cars:
        return ResponseModel(cars, "All cars have been retrieved")
    return ResponseModel(cars, "Empty list returned")


@router.get("/get/{id}", response_description="Single Car retrieve")
async def get_a_car(id):
    car = await retrieve_single_car(id)
    if car:
        return ResponseModel(car, "Car READ")
    return ErrorResponseModel("An error occurred.", 404, "Car is gone")


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


@router.delete("/del/{id}", response_description="Car deleted")
async def car_remover(id: str):
    car_to_be_deleted = await delete_car(id)
    if car_to_be_deleted:
        return ResponseModel("Car with register {} removed".format(id), "Deleted")
    return ErrorResponseModel("An error occurred", 404, "This is a real 404")
