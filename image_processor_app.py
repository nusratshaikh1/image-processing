import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np, cv2, io

st.title("🖼️ Image Processing: Enhance & Explore")
f = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if f:
    img = Image.open(f).convert("RGB")
    b = st.sidebar.slider("Brightness", 0.0, 3.0, 1.0)
    c = st.sidebar.slider("Contrast", 0.0, 3.0, 1.0)
    s = st.sidebar.slider("Saturation", 0.0, 3.0, 1.0)  # <-- renamed here
    
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)

    flt = st.sidebar.selectbox("Filter", ["None", "Grayscale", "Edge Detection"])
    np_img = np.array(img)
    if flt == "Grayscale":
        np_img = cv2.cvtColor(cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
    elif flt == "Edge Detection":
        edges = cv2.Canny(cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY), 100, 200)
        np_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    flip = st.sidebar.radio("Flip", ["None", "Horizontal", "Vertical"])
    out = Image.fromarray(np_img)
    if flip == "Horizontal":
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip == "Vertical":
        out = out.transpose(Image.FLIP_TOP_BOTTOM)

    c1, c2 = st.columns(2)
    c1.image(Image.open(f), caption="Original", use_container_width=True)
    c2.image(out, caption="Edited", use_container_width=True)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    st.download_button("💾 Download", buf.getvalue(), "edited.png", "image/png")
else:
    st.info("👆 Upload an image to start!")
