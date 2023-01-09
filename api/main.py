from fastapi import FastAPI

from . import (
    availability,
    clients,
    employees,
    products,
    purchases,
    stores,
    warehouse,
    works,
)

API_VERSION = "1.0.1"
TITLE = "Supermercado API"

app = FastAPI(title=TITLE, version=API_VERSION)

@app.get("/")
def root():
    return {"health_check": "OK", "version": API_VERSION}

# Include remaining path operations.
app.include_router(availability.router)
app.include_router(clients.router)
app.include_router(employees.router)
app.include_router(products.router)
app.include_router(purchases.router)
app.include_router(stores.router)
app.include_router(warehouse.router)
app.include_router(works.router)
