import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import user_router, login_router, warehouse_router, product_router, transaction_router, client_router, \
    alert_router

app = FastAPI(title="Stockify.API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por los dominios específicos si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Including routers to handle different endpoints
app.include_router(user_router.router)
app.include_router(warehouse_router.router)
app.include_router(product_router.router)
app.include_router(transaction_router.router)
app.include_router(client_router.router)
app.include_router(alert_router.router)
app.include_router(login_router.router)

# Running the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
