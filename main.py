import streamlit as st
from chatbot import HiringAssistant

def main():
    st.title("TalentScout Hiring Assistant Chatbot")
    st.markdown("""
    Welcome to TalentScout's Hiring Assistant! This chatbot will help screen candidates for technology positions by gathering essential information and assessing technical proficiency.
    """)

    # Initialize chatbot in session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistant()

    # Display chat messages
    for message in st.session_state.chatbot.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.chatbot.process_input(prompt)
        st.rerun()

if __name__ == "__main__":
    main()