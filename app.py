import streamlit as st
import requests

# create the title for the page
st.title("🤝 Your Personal Assistant")

# add subheader
st.subheader("What can your personal assistant do?")

# create a list of what your assistant can do
st.markdown("""
            1. Answer questions on various topics.   
            2. Arrange Calendar events and meetings.  
            3. Read your emails and send replies, can even summarize them for you.
            4. Manage your tasks and to-do lists.
            5. Take quick notes for you.
            6. Track your expenses and budgeting.
            """)

# add chats subheader
st.subheader("💬 Chat with your assistant")

# create a session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show the messages in chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# create a chat input box
user_message = st.chat_input()

      
# if user sends a message
if user_message:
    with st.chat_message("user"):
        st.markdown(user_message)
        # append the user message to message history
        st.session_state.messages.append({"role": "user", "content": user_message})
    
    # send the user message to the n8n webhook
    with st.spinner("🤔 Thinking..."):
        try:
            response = requests.post(
                "https://muhammadmahad.app.n8n.cloud/webhook/27bdde11-8263-469c-82ae-c42e7b4232ea",
                json={"msg": user_message},
                timeout=120  # AI Agent can take time with many tools
            )
        except requests.exceptions.Timeout:
            ai_response = "⚠️ Request timed out. The AI Agent took too long to respond."
            response = None
        except requests.exceptions.ConnectionError:
            ai_response = "⚠️ Could not connect to the n8n webhook. Is your n8n instance running?"
            response = None
    
    # get the AI response from webhook
    if response is not None:

        if response.status_code != 200:
            ai_response = f"⚠️ Webhook returned status {response.status_code}: {response.text}"
        elif not response.text.strip():
            ai_response = "⚠️ Webhook returned an empty response. Make sure your n8n workflow is **Active** (not just saved)."
        else:
            try:
                data = response.json()
                ai_response = data[0]["output"]
            except (requests.exceptions.JSONDecodeError, KeyError, IndexError) as e:
                ai_response = f"⚠️ Unexpected response format: {response.text[:500]}"
    
    # display the AI response in chat
    with st.chat_message("assistant"):
        st.markdown(ai_response)
        # append the AI response to message history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})