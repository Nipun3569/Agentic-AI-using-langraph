from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,HumanMessage
import operator
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

llm=ChatOllama(model="gemma:2b")

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {"messages": [response]}

#checkpointer
checkpointer=InMemorySaver()

graph=StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot=graph.compile(checkpointer=checkpointer)

