from fastapi import FastAPI

from server import routes

app = FastAPI()
app.include_router(routes.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


    