# from langchain_groq import ChatGroq
# from API.config import settings
# from .state import State
# from API.tools import add_device, query_devices
# from langchain_core.messages import (
#     SystemMessage,
#     AIMessage,
#     HumanMessage,
#     RemoveMessage,
# )
# from .prompts import ASSISTANT_PROMPT,DATA_MANAGER_PROMPT
# from langgraph.types import Command
# from pydantic import SecretStr

# llm = ChatGroq(api_key=SecretStr(settings.GROQ_API_KEY), model="llama-3.3-70b-versatile")
# llm_with_tools =llm.bind_tools([add_device,query_devices])


# def Assistant(state: State) -> State:
#     response: AIMessage=llm.invoke(input=[SystemMessage(content=ASSISTANT_PROMPT)]+state["messages"])
#     return {"messages":[response]}


# def DataManager(state: State) -> State:
#     response: AIMessage=llm_with_tools.invoke(input=[SystemMessage(content=DATA_MANAGER_PROMPT)]+state["messages"])
#     return {"messages":[response]}