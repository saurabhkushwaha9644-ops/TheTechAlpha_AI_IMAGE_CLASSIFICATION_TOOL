import os
# To hide unnecessary TensorFlow warnings in terminal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from PIL import Image
import fitz  # PyMuPDF
import io
import sqlite3

# Page configuration
st.set_page_config(page_title="The Tech Alpha", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* White background for the main app */
    .stApp { 
        background-color: #FFFFFF !important; 
        color: #111111 !important; 
    }
    /* Light gray background for sidebar for neat contrast */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E5E7EB;
    }
    /* Style for the chat input box */
    .stChatInput { 
        background-color: #FFFFFF !important; 
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important; 
        color: #111111 !important;
    }
    /* Make all texts dark/black for high readability */
    h1, h2, h3, p, span, label {
        color: #111111 !important;
    }
    </style>
""", unsafe_allow_html=True)

conn = sqlite3.connect('chat_history.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS global_chats (role TEXT, content TEXT)''')
conn.commit()

@st.cache_resource
def load_model(model_name):
    if model_name == "ResNet50 (More Accurate)":
        return ResNet50(weights='imagenet')
    return MobileNetV2(weights='imagenet')

# Image Classification Logic
def classify_now(pil_img, model_name):
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    resized_img = pil_img.resize((224, 224))
    x = image.img_to_array(resized_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    current_model = load_model(model_name)
    predictions = current_model.predict(x, verbose=0)
    return decode_predictions(predictions, top=3)

if "messages_loaded" not in st.session_state:
    c.execute("SELECT role, content FROM global_chats")
    rows = c.fetchall()
    st.session_state.messages = [{"role": r, "content": cnt} for r, cnt in rows]
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your professional AI Image Assistant. Please upload an image/PDF from the left panel or capture a live photo."}]
    st.session_state.messages_loaded = True

st.title("🤖 AI Image Assistant")
st.caption("With Chat Memory and Multi-Model Support.")
st.write("---")

with st.sidebar:
    st.header("⚙️ Settings Panel")
    selected_model = st.selectbox("Choose AI Model:", ["MobileNetV2 (Fast & Light)", "ResNet50 (More Accurate)"])
    st.write("---")
    mode = st.radio("Input Source:", ["Upload File (PDF/JPG/PNG)", "Live Camera"])
    
    st.write("---")

    if st.button("🗑️ Clear Chat History"):
        c.execute("DELETE FROM global_chats")
        conn.commit()
        st.session_state.clear()
        st.rerun()

    uploaded_file = None
    pil_image_to_process = None
    
    if mode == "Upload File (PDF/JPG/PNG)":
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png", "pdf"])
        if uploaded_file:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext == 'pdf':
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                page = doc.load_page(0)
                pix = page.get_pixmap(dpi=150)
                pil_image_to_process = Image.open(io.BytesIO(pix.tobytes("png")))
            else:
                pil_image_to_process = Image.open(uploaded_file)
    else:
        camera_image = st.camera_input("Take a Photo")
        if camera_image:
            pil_image_to_process = Image.open(camera_image)

    if pil_image_to_process is not None:
        if st.button("🚀 Send for Analysis"):
            st.session_state.messages.append({"role": "user", "content": "🔄 I have submitted a new image for analysis."})
            c.execute("INSERT INTO global_chats VALUES (?, ?)", ("user", "🔄 I have submitted a new image for analysis."))
            
            with st.spinner("AI is analyzing the image..."):
                results = classify_now(pil_image_to_process, selected_model)
            
            res_list = [{"label": l.replace('_', ' ').title(), "score": float(s)*100} for _, l, s in results[0]]
            
            bot_text = f"📊 **Analysis Results ({selected_model}):**\n\n"
            for r in res_list:
                bot_text += f"- **{r['label']}**: {r['score']:.2f}%\n"
                
            st.session_state.messages.append({"role": "assistant", "content": bot_text})
            c.execute("INSERT INTO global_chats VALUES (?, ?)", ("assistant", bot_text))
            conn.commit()
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_text := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_text})
    c.execute("INSERT INTO global_chats VALUES (?, ?)", ("user", user_text))
    with st.chat_message("user"):
        st.write(user_text)
        
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            response = "I received your message. I am an image classification tool. Please upload an image or PDF file from the left sidebar to get instant predictions."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            c.execute("INSERT INTO global_chats VALUES (?, ?)", ("assistant", response))
            conn.commit()
