from typing import Optional
from pydantic import BaseModel, Field

class CarSchema(BaseModel):
    owner: str = Field(...)
    manufacturer: str = Field(...)
    year: int = Field(..., gt=0, lt=21)

    class Config:
        schema_extra = {
            "example": {
                "owner": "Jorjola",
                "manufacturer": "Ferrari",
                "year": 12,
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
                "year": 17,
            }
        }
