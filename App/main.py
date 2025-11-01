from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=8000)
    server = uvicorn.Server(config)
    server.run()
