from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage
from API.agent import graph  
from API.db import init_db
from API.tools import add_device, query_devices
from API.schemas import AskRequest
from fastapi import FastAPI, Body
from rich import print


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    await init_db()
    print("Database initialized.")
    yield
    print("Application is shutting down...")


API_VERSION = "v1"

app = FastAPI(
    lifespan=lifespan,
    title="Samsung Phone Advisor",
    version=API_VERSION,
    description="A smart assistant for Samsung phone recommendations, powered by LangGraph.",
)

api_prefix = f"/api/{API_VERSION}"



@app.post(f"{api_prefix}/ask", tags=["Assistant"])
async def ask(payload: AskRequest = Body(...)):
    """
    Receives a natural language question and returns a synthesized answer.
    """
    query = payload.question
    print(f"Received query: {query}")

    inputs = {"messages": [HumanMessage(content=query)]}
    
    response_content = ""
    async for event in graph.astream(inputs):
        if "agent" in event:
            response_messages = event["agent"].get("messages", [])
            if response_messages:
                last_message = response_messages[-1]
                if not last_message.tool_calls:
                    response_content = last_message.content

    return {"answer": response_content}

@app.post(f"{api_prefix}/add_device/{{model_name}}", tags=["Admin"])
async def add_device_route(model_name: str):
    return await add_device(model_name=model_name)


@app.get(f"{api_prefix}/query_devices", tags=["Admin"])
async def query_devices_route(where_clause: str):
    return await query_devices(where_clause=where_clause)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the Samsung Phone Advisor API {API_VERSION}"}