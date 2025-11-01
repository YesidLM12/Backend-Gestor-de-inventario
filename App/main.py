from fastapi import FastAPI
import uvicorn
from app.db.init_db import init_db
from app.api.v1.router import api_router

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8000)
    server = uvicorn.Server(config)
    server.run()
