import streamlit as st
from pathlib import Path

# 1. Get the directory where 3.py is located
script_dir = Path(__file__).parent
st.title("GHOST OF TSUSHIMA")
# 2. Build the path to the image
image_path = script_dir / "image.jpg"


pressed = st.button("GHOST")
if pressed:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        st.image(image_bytes, caption="Background Image")
    st.balloons()