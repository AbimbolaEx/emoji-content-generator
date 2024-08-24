import streamlit as st
import requests
import time

# FastAPI backend URL
API_URL = "https://emoji-content-generator.onrender.com"  # Replace with your Render deployment URL



st.title("Emoji Content Generator")

# Function to get available models
def get_models():
    try:
        response = requests.get(f"{API_URL}/models", timeout=5)
        if response.status_code == 200:
            return response.json()["available_models"]
        else:
            st.error(f"Failed to fetch models. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API. Please ensure the backend server is running.")
    except requests.exceptions.Timeout:
        st.error("Request to API timed out. Please check your connection and try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
    return []

# Fetch available models
models = get_models()

# Sidebar for model selection
selected_model = st.sidebar.selectbox("Choose a model", models)

# Main content area
st.header("Generate Content from Emojis")

# Input for emojis
emojis = st.text_input("Enter emojis (separated by spaces)", "😊 🌞 🏖️")

if st.button("Generate Content"):
    # Prepare the request
    data = {
        "emojis": emojis.split(),
        "model": selected_model
    }
    
    # Send request to FastAPI backend
    response = requests.post(f"{API_URL}/generate-content", json=data)
    
    if response.status_code == 200:
        content = response.json()["generated_content"]
        st.success("Content generated successfully!")
        
        # Typing effect with improved speed and text wrapping
        typed_content = st.empty()  # Create a placeholder for the typing effect
        full_content = ""
        for char in content:
            full_content += char
            typed_content.markdown(f"<div style='white-space: pre-wrap;'>{full_content}</div>", unsafe_allow_html=True)
            time.sleep(0.01)  # Adjusted typing speed for faster output
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

st.header("Chat with AI")

# Input for chat
user_input = st.text_input("Enter your question")

if st.button("Send"):
    # Prepare the request
    data = {
        "question": user_input,
        "model": selected_model
    }
    
    # Send request to FastAPI backend
    response = requests.post(f"{API_URL}/chat", json=data)
    
    if response.status_code == 200:
        content = response.json()["response"]
        st.success("Response received!")
        
        # Typing effect with improved speed and text wrapping
        typed_content = st.empty()  # Create a placeholder for the typing effect
        full_content = ""
        for char in content:
            full_content += char
            typed_content.markdown(f"<div style='white-space: pre-wrap;'>{full_content}</div>", unsafe_allow_html=True)
            time.sleep(0.01)  # Adjusted typing speed for faster output
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

# Display information about the selected model
st.sidebar.write(f"Selected model: {selected_model}")
