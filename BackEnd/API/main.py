from contextlib import asynccontextmanager

from API.agent import graph
from API.db import init_db
from API.tools import add_device, query_devices

# from API.db import
from fastapi import FastAPI
from rich import print


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    await init_db()
    yield
    print("Application is shutting down...")


API_VERSION = "v1"


app = FastAPI(
    lifespan=lifespan,
    title="Smart Assistant",
    version=API_VERSION,
    description="Smart Assistant API",
)

api_prefix = f"/{API_VERSION}"


@app.get("/ask")
async def ask(query: str):
    return {"response": query}


@app.get("/add_device/{model_name}")
async def add_device_route(model_name: str):
    return await add_device(model_name=model_name)


@app.get("/query_devices")
async def query_devices_route(where_clause: str):
    print(where_clause)
    return await query_devices(where_clause)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to Price Pilot API {API_VERSION}"}
