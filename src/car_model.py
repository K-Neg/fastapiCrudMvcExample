from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class CarSchema(BaseModel):
    owner: str = Field(...)
    manufacturer: str = Field(...)
    year: int = Field(..., gt=0, lt=9)

    class Config:
        schema_extra = {
            "example": {
                "owner": "Jorjola",
                "manufacturer": "Ferrari",
                "year": 2,
            }
        }


class UpdateCarModel(BaseModel):
    owner: Optional[str]
    manufacturer: Optional[str]
    year: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "owner": "Mau Mau",
                "manufacturer": "Ford",
                "year": 4,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}