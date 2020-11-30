from pydantic import BaseModel

class ClientSchema(BaseModel):
    name: str
    age: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Anna",
                "age": 12,
            }
        }   