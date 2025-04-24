# module2.py (Gemini Chatbot)
import os
import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF processing
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API Key not found. Make sure it's set in the .env file.")

# Configure Gemini AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

def run_module_2():
    # Main function for Module 2
    st.title("Multimodal Chatbot with Gemini Flash ⚡️")
    st.caption("Chat with Google's Gemini Flash model using images, PDFs, and text input.")
    
    # Sidebar for file upload
    uploaded_file = st.file_uploader("Upload an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])
    
    pdf_text = None
    uploaded_image = None

    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension in ["jpg", "jpeg", "png"]:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        elif file_extension == "pdf":
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf:
                pdf_text = "\n".join([page.get_text("text") for page in pdf])
            st.success("PDF uploaded successfully. Extracted text will be used for responses.")
    
    # Chat UI - Display history
    chat_placeholder = st.container()
    with chat_placeholder:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    prompt = st.chat_input("Ask something...")

    if prompt:
        inputs = [prompt]
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)

        if uploaded_image:
            inputs.append(uploaded_image)

        if pdf_text:
            inputs.append(pdf_text)

        with st.spinner("Generating response..."):
            response = model.generate_content(inputs)

        with chat_placeholder:
            with st.chat_message("assistant"):
                st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})

    if uploaded_file and not prompt:
        st.warning("Please enter a text query to analyze the uploaded file.")
