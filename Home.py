import streamlit as st
from PIL import Image

# Title
st.write("# Welcome to my classroom")

# Use the uploaded file path
uploaded_image_path = "/mnt/data/image.png"

# Load and display the uploaded image
try:
    image = Image.open(uploaded_image_path)
    st.image(image, caption="A friendly teacher welcoming you!")
except FileNotFoundError:
    st.write("⚠️ Image file not found! Please upload a valid image.")
