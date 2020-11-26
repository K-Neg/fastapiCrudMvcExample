import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cars

parked = database.get_collection("parked")


def car_db_to_dict(car) -> dict:
    return {
        "id": str(car["_id"]),
        "owner": car["owner"],
        "manufacturer": car["manufacturer"],
        "year": car["year"],
    }


async def add_car(car_data: dict) -> dict:
    car = await parked.insert_one(car_data)
    new_car = await parked.find_one({"_id": parked.inserted_id})
    return car_db_to_dict(new_car)


async def retrieve_all_cars():
    cars = []
    # a error can occur over here due to 'asyncness'
    async for car in parked.find():
        cars.append(car_db_to_dict(car))
    return cars


# get a single car
async def retrieve_single_car(id: str) -> dict:
    car = await parked.find_one({"_id": ObjectId(id)})
    if car:
        return car_db_to_dict(car)


# Update a specific CAR
async def update_car(id: str, data: dict):
    if len(data) < 1:
        return False
    car = await parked.find_one({"_id": ObjectId(id)})
    if car:
        updated_car = await parked.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_car:
            return True
        return False


# Delete a car
async def delete_car(id: str):
    car = await parked.find_one({"_id": ObjectId(id)})
    if car:
        await parked.delete_one({"_id": ObjectId(id)})
        return True