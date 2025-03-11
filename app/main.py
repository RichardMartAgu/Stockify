import uvicorn
from fastapi import FastAPI

from app.routers import user_router, login_router

app = FastAPI(title="Stockify.API")

app.include_router(user_router.router)
app.include_router(login_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
