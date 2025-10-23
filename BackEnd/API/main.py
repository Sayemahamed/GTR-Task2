from contextlib import asynccontextmanager

from API.agent import graph

# from API.db import
from fastapi import FastAPI
from rich import print
from API.db import init_db,Device
from API.tools import add_device,get_device


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
    print(graph.invoke({"count": [0]}))
    return {"response": query}


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to Price Pilot API {API_VERSION}"}
