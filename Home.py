import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Title
st.write("# Welcome to my classroom")

# URL of the image
image_url = "https://raw.githubusercontent.com/kwonsungja/My-homepy/main/images/%ED%99%88%ED%94%BC%EC%82%AC%EC%A7%84.png"

# Load and display the image from the URL
try:
    response = requests.get(image_url)
    response.raise_for_status()  # Ensure the request was successful
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="A friendly teacher welcoming you!")
except requests.exceptions.RequestException as e:
    st.write(f"⚠️ Unable to load the image from the URL! Error: {e}")
except Exception as e:
    st.write(f"⚠️ An error occurred while processing the image. Error: {e}")

