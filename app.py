import streamlit as st
import openai
from prompts import *
from utils import *
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize session state
def init_session():
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
        st.session_state.stage = "greeting"
        st.session_state.candidate_info = {
            "name": "", "email": "", "phone": "",
            "experience": "", "position": "", 
            "location": "", "tech_stack": []
        }

# Configure page
st.set_page_config(
    page_title="TalentScout AI Hiring Assistant",
    page_icon="",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.stChatInput {position: fixed; bottom: 1rem;}
.stChatMessage {padding: 1rem;}
</style>
""", unsafe_allow_html=True)

# Main app
def main():
    init_session()
    
    st.title("TalentScout AI Hiring Assistant ")
    st.caption("Powered by AI - Initial Screening Tool")
    
    # Chat container
    with st.container(height=500, border=False):
        for msg in st.session_state.conversation:
            if msg["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])
    
    # Conversation handler
    def handle_response(user_input):
        user_input = user_input.strip()
        
        # Exit condition
        if any(word in user_input.lower() for word in ["exit", "quit", "bye", "stop"]):
            st.session_state.stage = "conclusion"
        
        if st.session_state.stage == "greeting":
            response = get_greeting()
            st.session_state.stage = "get_name"
        
        elif st.session_state.stage == "get_name":
            st.session_state.candidate_info["name"] = user_input
            response = "Thank you! What's your email address?"
            st.session_state.stage = "get_email"
        
        elif st.session_state.stage == "get_email":
            if validate_email(user_input):
                st.session_state.candidate_info["email"] = user_input
                response = "Got it! And your phone number?"
                st.session_state.stage = "get_phone"
            else:
                response = "Please enter a valid email address (e.g., name@example.com)"
        
        elif st.session_state.stage == "get_phone":
            if validate_phone(user_input):
                st.session_state.candidate_info["phone"] = user_input
                response = "How many years of professional experience do you have?"
                st.session_state.stage = "get_experience"
            else:
                response = "Please enter a valid phone number (at least 8 digits)"
        
        elif st.session_state.stage == "get_experience":
            st.session_state.candidate_info["experience"] = user_input
            response = "What position are you applying for?"
            st.session_state.stage = "get_position"
        
        elif st.session_state.stage == "get_position":
            st.session_state.candidate_info["position"] = user_input
            response = "Where are you currently located?"
            st.session_state.stage = "get_location"
        
        elif st.session_state.stage == "get_location":
            st.session_state.candidate_info["location"] = user_input
            response = get_tech_stack_prompt()
            st.session_state.stage = "get_tech_stack"
        
        elif st.session_state.stage == "get_tech_stack":
            tech_stack = [t.strip() for t in user_input.split(",") if t.strip()]
            st.session_state.candidate_info["tech_stack"] = tech_stack
            response = generate_technical_questions(tech_stack)
            st.session_state.stage = "technical_questions"
        
        elif st.session_state.stage == "technical_questions":
            response = "Thank you for your answers! Type anything to conclude."
            st.session_state.stage = "conclusion"
        
        elif st.session_state.stage == "conclusion":
            save_conversation(st.session_state.conversation)
            response = get_conclusion()
        
        return response

    # User input
    if user_input := st.chat_input("Type your message here..."):
        st.session_state.conversation.append({"role": "user", "content": user_input})
        bot_response = handle_response(user_input)
        st.session_state.conversation.append({"role": "assistant", "content": bot_response})
        st.rerun()

if __name__ == "__main__":
    main()