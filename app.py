import cv2
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np

# Load the dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)

colors = load_colors()

# Function to find closest color name
def get_color_name(R, G, B):
    min_dist = float('inf')
    cname = "Unknown"
    for _, row in colors.iterrows():
        d = abs(R - int(row.R)) + abs(G - int(row.G)) + abs(B - int(row.B))
        if d < min_dist:
            min_dist = d
            cname = row.color_name
    return cname

st.title("🎨 Color Detection App")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_array = np.array(img)
    st.image(img, caption='Uploaded Image', use_column_width=True)

    st.write("Click anywhere on the image (X, Y) coordinates to detect color.")

    # Capture click
    if 'click_coords' not in st.session_state:
        st.session_state.click_coords = None

    def callback():
        st.session_state.click_coords = (st.session_state.x, st.session_state.y)

    st.number_input("X", key="x", min_value=0, max_value=img_array.shape[1]-1, step=1, on_change=callback)
    st.number_input("Y", key="y", min_value=0, max_value=img_array.shape[0]-1, step=1, on_change=callback)

    if st.session_state.click_coords:
        x, y = st.session_state.click_coords
        pixel = img_array[y, x]
        R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
        color_name = get_color_name(R, G, B)
        st.markdown(f"### 🎯 Detected Color: `{color_name}`")
        st.markdown(f"**RGB:** ({R}, {G}, {B})")
        st.markdown(f"<div style='background-color: rgb({R}, {G}, {B}); width: 100px; height: 50px;'></div>", unsafe_allow_html=True)
