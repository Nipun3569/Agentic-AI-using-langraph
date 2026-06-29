import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
CONFIG= {'configurable':{'thread_id':'thread-1'}}

#************************************Utility Functions*********************************************
def generate_threadid():
    thread_id=uuid.uuid4()
    return thread_id

#*************************************Session setup************************************************
#{'role':'user',content:hi}
message_history=[]
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
#st . session_state-> dict that doesnt get erase when we press enter, it gets erased when we refresh page

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_threadid()
    
#**************************************Sidebar Ui*************************************

st.sidebar.title('LangGraph Chatbot')

st.sidebar.button('New Chat')

st.sidebar.header('My Conversations')
#loading conversation hsitory
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input('Type here...')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.text(user_input)

    
   
    
    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config={'configurable':{'thread_id':'thread-1'}},
            stream_mode='messages'  
            )
        )
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})


