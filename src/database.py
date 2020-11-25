import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = "mongodb://localhost:8000"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cars

cars_objs = database.get_collection("car_parkeds")


def car_db_to_dict(car) -> dict:
    return {
        "id": str(car["id"]),
        "owner": car["name"],
        "manufacturer": car["manufacturer"],
        "year": car["year"],
    }


# add new car
async def add_car(car_data: dict) -> dict:
    car = await cars_objs.insert_one(car_data)
    new_car = await cars_objs.find_one({"_id": cars_objs.inserted_id})
    return car_db_to_dict(new_car)


async def retrieve_all_cars():
    cars = []
    # a error can occur over here due to 'asyncness'
    async for car in cars_objs.find():
        cars.append(car_db_to_dict(car))
    return cars


# get a single car
async def retrieve_single_car(id: str) -> dict:
    car = await cars_objs.find_one({"_id": ObjectId(id)})
    if car:
        return car_db_to_dict(car)


# Update a specific CAR
async def update_car(id: str, data: dict):
    if len(data) < 1:
        return False
    car = await cars_objs.find_one({"_id": ObjectId(id)})
    if car:
        updated_car = await cars_objs.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_car:
            return True
        return False


# Delete a car
async def delete_car(id: str):
    car = await cars_objs.find_one({"_id": ObjectId(id)})
    if car:
        await cars_objs.delete_one({"_id": ObjectId(id)})
        return True