import streamlit as st
from SimpleChatBot import chatmodel

st.title("💬 Simple Chatbot")
st.divider()

# First Way to disply message using st.chat_input()
# input = st.chat_input(placeholder='Enter your text...')
# if input:
#     st.write(chatmodel(input))

# Second Way to disply message using st.chat_input()
# if input := st.chat_input(placeholder='Ask Anything'):
#     st.write(chatmodel(input))

# Define Message
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Message
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.write(msg["content"])

# chat input
if user_input := st.chat_input(placeholder='Ask anything'):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "avatar": "👨"
        }
    )
    st.chat_message("user", avatar="👨").write(user_input)

    # Simple Chatbot Response
    response = chatmodel(user_input)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
            "avatar": "🤖"
        }
    )
    st.chat_message("assistant", avatar="🤖").write(response)