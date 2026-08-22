import streamlit as st
from prompts import *
from google import genai
from google.genai import types
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()



if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1" : []}
    st.session_state.current_chat = "Chat 1"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "task" not in st.session_state:
    st.session_state.task = "document"

if "prompting" not in st.session_state:
    st.session_state.prompting = False

## GEMINI DETAIL
client = genai.Client(api_key=os.getenv("API_KEY"))

model = os.getenv("MODEL")

st.set_page_config(
    page_title="Nyaya AI",
    page_icon="icon.png",
)

### 
with st.sidebar:
    st.markdown(
        "<div style='text-align: center;'>",
        unsafe_allow_html=True
    )
    st.image(
    "logo.png",
    width=270
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <h1 style="margin-top:0; font-size:100;">Nyaya AI</h1>
        <p style="color:#9ca3af;">Here to help you</p>
    </div>
    """, unsafe_allow_html=True)

    placeholder = st.empty()

    def add_new_chat():
        index = len(st.session_state.chats.keys()) + 1
        st.session_state.chats[f"Chat {index}"] = []
        st.session_state.current_chat = f"Chat {index}"


    def switch_chat(name):
        st.session_state.current_chat = name

    def clear_ses():
        st.session_state.clear()
        st.rerun()

    btn0 = st.button("Clear Session", on_click=clear_ses, use_container_width=True)
    btn1 = st.button("New Chat", on_click=add_new_chat, use_container_width=True)

    c_index = 0
    max_index = len(st.session_state.chats.keys())
    for i in range(max_index):
        
        btn = st.button(f"Chat {int(max_index-c_index)}", on_click=switch_chat,
                        args=(f"Chat {int(max_index-c_index)}", ), use_container_width=True)
        c_index += 1






with st.bottom:
    # option = st.selectbox("TASK: ", ["Document","Legal", "Civic"])
    option = st.segmented_control("TASK: ", ["Document","Legal", "Civic"], width="stretch", label_visibility="collapsed")

    if option:
        st.session_state.task = option.lower()


    if st.session_state.task != "document":
        if st.session_state.prompting:
            query = st.chat_input("Write your query here!", submit_mode="disable")
        else:
            query = st.chat_input("Write your query here!")

        if query:
            messages = st.session_state.chats[st.session_state.current_chat]
            messages.append({
                "person":"user",
                "content":query,
                "task":st.session_state.task,
                "time":datetime.now().strftime("%I: %M %p")
            })
            messages.append({
                "person":"ai",
                "content":None, 
                "prompt":query,
                "task":st.session_state.task,
                "time":datetime.now().strftime("%I: %M %p")
            })
            st.session_state.prompting = True
    else:
        if st.session_state.prompting:
            query = st.chat_input("Write your query here!",
                                accept_file=True,
                                file_type=["pdf", "jpg", "png"], submit_mode="disable")
        else:
            query = st.chat_input("Write your query here!",
                                accept_file=True,
                                file_type=["pdf", "jpg", "png"])
        

        if query:
            messages = st.session_state.chats[st.session_state.current_chat]
            messages.append({
                "person":"user",
                "content":query.text,
                "task":st.session_state.task,
                "files":query.files,
                "time":datetime.now().strftime("%I: %M %p")
            })

            messages.append({
                "person":"ai",
                "content":None, 
                "prompt":query.text,
                "files":query.files,
                "task":st.session_state.task,
                "time":datetime.now().strftime("%I: %M %p")
            })
            st.session_state.prompting = True

## drawing the chat area
messages = st.session_state.chats[st.session_state.current_chat]
for i in range(len(messages)):

    if messages[i]["person"] == "ai":
        data = messages[i]

        with st.chat_message("assistant"):
            content = data['content']

            if content:
                st.markdown(content)
                st.caption(data["task"].capitalize())
                st.caption(data["time"])
            else:
                with st.spinner("Thinking.."):
                    if data["task"] == "document":
                        files = []
                        for f in data['files']:
                            files.append(types.Part.from_bytes(data=f.getvalue(), mime_type="application/pdf"),)

                        content = files.copy()
                        content.extend(merge(BASE_PROMPT, DOCUMENT_PROMPT).format(data["prompt"]))

                        response = client.models.generate_content(
                            model=model,
                            contents=content
                        )

                        st.session_state.prompting = False


                        messages[i]["content"] = response.text

                    else:
                        if data["task"] == "legal":
                            content = merge(BASE_PROMPT, LEGAL_PROMPT).format(data["prompt"])
                        if data["task"] == "civic":
                            content = merge(BASE_PROMPT, CIVIC_PROMPT).format(data["prompt"])

                        response = client.models.generate_content(
                            model=model,
                            contents=content
                        )

                        st.session_state.prompting = False

                        messages[i]["content"] = response.text

                    st.markdown(messages[i]["content"])
                    st.caption(data["task"].capitalize())
                    st.caption(data["time"])



    else:
        with st.chat_message("user"):
            data = messages[i]
            st.write(messages[i]['content'])
            st.caption(data["task"].capitalize())
            st.caption(data["time"])



            # if st.session_state.messages[i]['task'] == "document":
            #     st.pdf(st.session_state.messages[i]['files'][0])

