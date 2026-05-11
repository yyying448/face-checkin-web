import os
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import face_recognition
import pickle
import datetime
import pandas as pd  # 新增：用于保存数据

# --- 0. 全局存储配置 ---
LOG_FILE = "attendance_log.csv"  # 签到记录保存到这个文件

@st.cache_resource
def get_global_attendance():
    """
    创建一个全服务器共享的字典。
    只要程序不彻底停止，所有访问者共享这个数据。
    同时，初始化时会尝试从本地 CSV 加载历史记录。
    """
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(LOG_FILE)
            # 将 CSV 转回字典格式 {姓名: 时间}
            return dict(zip(df['name'], df['time']))
        except:
            return {}
    return {}

# 获取全局共享的签到字典
global_attendance = get_global_attendance()

def save_to_file(name, time_str):
    """将单条签到成功记录追加到本地文件"""
    df = pd.DataFrame([[name, time_str]], columns=['name', 'time'])
    df.to_csv(LOG_FILE, mode='a', index=False, header=not os.path.exists(LOG_FILE))

# --- 网页页面设置 ---
st.set_page_config(page_title="AI 面部签到系统", layout="wide")
st.title("🎓 班级智能签到系统 (网页版)")

# --- 1. 加载模型 ---
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

# --- 3. 主界面：摄像头输入 ---
st.info("提示：请使用 HTTPS 链接访问，否则无法调用摄像头。")
img_file = st.camera_input("请正对摄像头进行签到")

if img_file is not None:
    # 1. 获取图片字节流
    bytes_data = img_file.getvalue()
    
    # --- 第一重保险：检查字节流是否为空 ---
    if not bytes_data or len(bytes_data) == 0:
        st.error("无法获取图片数据，请重新拍照上传。")
    else:
        # 将字节流转为 numpy 数组
        nparr = np.frombuffer(bytes_data, np.uint8)
        # 2. 解码图片
        cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # --- 第二重保险：检查 OpenCV 是否成功解析了图片 ---
        if cv2_img is None:
            st.error("图片解析失败。可能是由于网络传输中断，请点击 'Clear photo' 后重试。")
        else:
            # 只有图片正常，才执行识别逻辑
            rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            
            # YOLO 检测
            results = yolo_model(cv2_img, conf=0.5, verbose=False)
            
            # ... 后面接你原本的 for box in results[0].boxes: 循环 ...
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face_crop = rgb_img[y1:y2, x1:x2]
        face_crop = np.ascontiguousarray(face_crop)
        
        encodings = face_recognition.face_encodings(face_crop)
        if encodings:
            face_enc = encodings[0]
            
            known_encs = []
            known_names = []
            for n, encs in face_db.items():
                known_encs.extend(encs)
                known_names.extend([n] * len(encs))
            
            distances = face_recognition.face_distance(known_encs, face_enc)
            if len(distances) > 0 and np.min(distances) < 0.4:
                name = known_names[np.argmin(distances)]
                
                # --- 核心修改：操作全局字典 ---
                if name not in global_attendance:
                    time_now = datetime.datetime.now().strftime("%H:%M:%S")
                    global_attendance[name] = time_now
                    save_to_file(name, time_now) # 实时写入硬盘
                    st.success(f"🎉 {name} 签到成功！")
                else:
                    st.info(f"💡 {name}，你已经签过到啦 ({global_attendance[name]})")
            else:
                st.warning("未能匹配到已知人脸，请重试。")

# --- 4. 显示名单 (侧边栏) ---
col1, col2 = st.sidebar.columns(2)
col1.metric("已签到", len(global_attendance))
col2.metric("未签到", len(all_names) - len(global_attendance))

tab1, tab2 = st.sidebar.tabs(["✅ 已签到", "❌ 未签到"])

with tab1:
    if global_attendance:
        for name, time in global_attendance.items():
            st.text(f"👤 {name} ({time})")
    else:
        st.write("目前暂无签到")

with tab2:
    not_attended = [name for name in all_names if name not in global_attendance]
    if not_attended:
        for name in not_attended:
            st.text(f"🔴 {name}")
    else:
        st.success("全员已到齐！")

st.sidebar.markdown("---")
# 清空按钮：需要同时清空内存和删除本地文件
if st.sidebar.button("清空所有记录"):
    global_attendance.clear()
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    st.rerun()