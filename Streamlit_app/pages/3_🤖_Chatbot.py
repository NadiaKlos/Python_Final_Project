import streamlit as st
from openai import OpenAI
st.set_page_config(
    page_title="Python Final Project",
    page_icon="📚",
)

st.sidebar.image("https://formation-continue.ehesp.fr/sites/default/files/styles/crop_actu_desktop_800x540/public/content/news/img/shutterstock_1917115745_0.jpg?h=4b45c30e&itok=UCzG6up_")
st.sidebar.markdown("## **Subject Area** :\n*__Health and Medicine__*")
st.sidebar.markdown("## **Dataset Characteristics** :\n*__Multivariate__*")
st.sidebar.markdown("## **Feature Type** :\n*__Categorical, Integer__*")

with st.sidebar:
    openai_api_key = "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"
    "[View the source of the dataset](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)"
    "[View the source code (GitHub)](https://github.com/NadiaKlos/Python_Final_Project)"
    
st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)