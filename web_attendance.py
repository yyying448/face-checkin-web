import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import face_recognition
import pickle
import datetime

# --- 网页页面设置 ---
st.set_page_config(page_title="AI 面部签到系统", layout="wide")
st.title("🎓 班级智能签到系统 (网页版)")

# --- 1. 加载模型（使用缓存避免重复加载，提高速度） ---
@st.cache_resource
def load_models_web():
    yolo = YOLO("yolo11n-face.pt")
    with open("face_db/encodings.pkl", "rb") as f:
        db = pickle.load(f)
    return yolo, db

yolo_model, face_db = load_models_web()
all_names = list(face_db.keys())

# --- 2. 侧边栏：签到统计 ---
st.sidebar.header("📊 实时签到统计")
if 'attendance' not in st.session_state:
    st.session_state.attendance = {} # 使用 session_state 保持网页刷新后的数据

# --- 3. 主界面：摄像头输入 ---
# Streamlit 自带的摄像头组件，非常适合做拍照签到
img_file = st.camera_input("请正对摄像头进行签到")

if img_file is not None:
    # 将上传的图片转为 OpenCV 格式
    bytes_data = img_file.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # YOLO 检测
    results = yolo_model(cv2_img, conf=0.5, verbose=False)
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face_crop = rgb_img[y1:y2, x1:x2]
        face_crop = np.ascontiguousarray(face_crop)
        # 人脸识别
        encodings = face_recognition.face_encodings(face_crop)
        name = "Unknown"
        if encodings:
            face_enc = encodings[0]
            # 这里的逻辑和你之前的一样
            known_encs = []
            known_names = []
            for n, encs in face_db.items():
                known_encs.extend(encs)
                known_names.extend([n] * len(encs))
            
            distances = face_recognition.face_distance(known_encs, face_enc)
            if len(distances) > 0 and np.min(distances) < 0.4:
                name = known_names[np.argmin(distances)]
                
                # 记录签到
                if name not in st.session_state.attendance:
                    st.session_state.attendance[name] = datetime.datetime.now().strftime("%H:%M:%S")
                    st.success(f"🎉 {name} 签到成功！")

# --- 4. 显示名单 ---
col1, col2 = st.sidebar.columns(2)
col1.metric("已签到", len(st.session_state.attendance))
col2.metric("未签到", len(all_names) - len(st.session_state.attendance))

st.sidebar.write("### 📝 最近签到名单")
for name, time in st.session_state.attendance.items():
    st.sidebar.text(f"✅ {name} - {time}")

if st.sidebar.button("清空今天记录"):
    st.session_state.attendance = {}
    st.rerun()