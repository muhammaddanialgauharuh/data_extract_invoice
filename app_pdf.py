from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image

import google.generativeai as genai

api_key = "AIzaSyBtu0dsz19zfMaF2u7u3JBy0ZtLLs2KQv4"
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get responses
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to setup image for processing
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Data Extraction Application")

# Sidebar for file upload
with st.sidebar:
    image = Image.open('techma.png')

    st.image(image, width=120)
    st.title("Data Extraction Application")
    input = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])
    submit = st.button("Extract Data")

# Main content area
col1, col2 = st.columns([6.5, 2.5])

with col1:
    st.title("Invoice Data Extraction")
    # Display the uploaded image with reduced size
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice Image.", use_column_width=True, output_format="JPEG")

with col2:
    # If the "Extract Data" button is clicked
    if submit:
        st.subheader("Extracted Data from Invoice")
        # Process the uploaded image
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response("Invoice Data Extraction", image_data, input)
            st.write(response)
        except FileNotFoundError as e:
            st.error(str(e))
