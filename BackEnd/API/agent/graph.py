from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.messages import SystemMessage

from .state import State
from API.tools import query_devices, add_device
from .prompts import AGENT_PROMPT
from API.config import settings

llm = ChatGroq(api_key=SecretStr(settings.GROQ_API_KEY), model="llama-3.3-70b-versatile")
tools = [query_devices, add_device]
llm_with_tools = llm.bind_tools(tools)

def call_model(state: State) -> State:
    """The primary node that decides what to do."""
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=AGENT_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: State) -> str:
    """Determines the next step after the LLM call."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "use_tools"
    return END

builder = StateGraph(State)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "use_tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

graph = builder.compile()