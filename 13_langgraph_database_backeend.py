from langgraph.graph import StateGraph,START, END
from typing import TypedDict, Literal, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,HumanMessage
import operator
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver

import sqlite3

llm=ChatOllama(model="gemma:2b")

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)

#checkpointer
#we need to make sqllite database to store the chat history
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot=graph.compile(checkpointer=checkpointer)

#test
CONFIG={'configurable':{'thread_id':'test_thread'}}

response=chatbot.invoke(
    {
        'messages':[HumanMessage(content="Hello, how are you?")]
    },
    config=CONFIG
)

print(response)