import streamlit as st

# Setting the page title and layout
st.set_page_config(page_title="Welcome", layout="centered")

# Welcome Message
st.write("# Welcome to my classroom!")
st.write("### It's my app and homepage 😊")

# Adding an image or visual element
st.image(
    "https://via.placeholder.com/800x400.png?text=Welcome+to+My+Classroom",
    caption="Your homepage image here",
)

# Interactive button
if st.button("Click me for a surprise!"):
    st.write("🎉 Surprise! You're awesome! 🎉")

# Footer
st.write("---")
st.write("Made with ❤️ using Streamlit")
