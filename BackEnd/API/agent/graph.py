from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from pydantic import SecretStr
from langchain_core.messages import SystemMessage, BaseMessage

from .state import State
from API.tools import query_devices, add_device
from .prompts import AGENT_PROMPT
from API.config import settings

# 1. Define the LLM and bind tools
llm = ChatGroq(api_key=SecretStr(settings.GROQ_API_KEY), model="llama-3.1-70b-versatile")
tools = [query_devices, add_device]
llm_with_tools = llm.bind_tools(tools)

# 2. Define the Agent Node
def call_model(state: State) -> State:
    """The primary node that decides what to do."""
    messages = state["messages"]
    # Add the system prompt only for the first turn
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=AGENT_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 3. Define the Tool Node
# The ToolNode from langgraph.prebuilt handles the execution of tools
tool_node = ToolNode(tools)

# 4. Define the Conditional Edge
def should_continue(state: State) -> str:
    """Determines the next step after the LLM call."""
    last_message = state["messages"][-1]
    # If the LLM made a tool call, route to the tool node
    if last_message.tool_calls:
        return "use_tools"
    # Otherwise, the LLM has responded to the user, so we end
    return END

# 5. Build the graph
builder = StateGraph(State)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
)
builder.add_edge("tools", "agent")

graph = builder.compile()