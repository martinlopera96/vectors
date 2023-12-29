import streamlit as st
import os

from process import *

st.title("Image to SVG Converter")
threshold_value = st.slider("Adjust Threshold", 0, 255, 128)

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpeg", "jpg", "bmp"])

if uploaded_file is not None:
    svg_output, svg_data = process_image(uploaded_file, threshold_value)
    st.markdown(f'<div style="width: 100%; height: auto;">{svg_data}</div>', unsafe_allow_html=True)

    original_file_name = os.path.splitext(uploaded_file.name)[0]
    download_file_name = f"resultado_{original_file_name}.svg"
    st.download_button(label="Download SVG",
                       data=svg_output,
                       file_name=download_file_name,
                       mime="image/svg+xml")
