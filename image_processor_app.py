import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np, cv2, io

st.title("🖼️ Simple Image Editor")
f = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if f:
    img = Image.open(f).convert("RGB")
    st.sidebar.subheader("Adjustments")
    b = st.sidebar.slider("Brightness", 0.0, 3.0, 1.0)
    c = st.sidebar.slider("Contrast", 0.0, 3.0, 1.0)
    s = st.sidebar.slider("Color", 0.0, 3.0, 1.0)
    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)

    st.sidebar.subheader("Filters")
    flt = st.sidebar.selectbox("Choose", ["None", "Grayscale", "Edge Detection"])
    np_img = np.array(img)
    if flt == "Grayscale":
        np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        np_img = cv2.cvtColor(np_img, cv2.COLOR_GRAY2RGB)
    elif flt == "Edge Detection":
        e = cv2.Canny(cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY), 100, 200)
        np_img = cv2.cvtColor(e, cv2.COLOR_GRAY2RGB)

    st.sidebar.subheader("Flip")
    flip = st.sidebar.radio("Flip Image", ["None", "Horizontal", "Vertical"])
    out = Image.fromarray(np_img)
    if flip == "Horizontal": out = out.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip == "Vertical": out = out.transpose(Image.FLIP_TOP_BOTTOM)

    c1, c2 = st.columns(2)
    c1.image(Image.open(f), caption="Original", width='stretch')
    c2.image(out, caption="Edited", width='stretch')

    buf = io.BytesIO(); out.save(buf, format="PNG")
    st.download_button("💾 Download", buf.getvalue(), "edited.png", "image/png")
else:
    st.info("👆 Upload an image to start!")
