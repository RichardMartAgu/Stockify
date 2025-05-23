import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Stockify.API")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
