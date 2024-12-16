import streamlit as st
import os

# Title
st.write("# Welcome to my classroom")

# Check if the image exists in the current directory
image_path = "image.png"

if os.path.exists(image_path):
    # Display the image with a caption
    st.image(image_path, caption="A friendly teacher welcoming you!")
else:
    st.write("⚠️ Image file not found! Please make sure 'image.png' is in the same folder as this script.")
streamlit run app.py
