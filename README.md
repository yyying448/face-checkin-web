# 🎓 全班人脸识别签到系统 (Web 版)

这是一个基于 **YOLOv11** 和 **Face Recognition** 开发的智能签到系统。

### 🚀 功能特点
* **快速识别**：利用 YOLOv11 进行人脸检测，识别精度高。
* **网页化部署**：基于 Streamlit 开发，无需安装环境，点开网址即可签到。
* **实时统计**：自动统计已到人数与未到人数，支持签到记录展示。

### 🛠️ 技术栈
* **后端**: Python 3.10+
* **AI 模型**: YOLOv11, dlib (face_recognition)
* **界面**: Streamlit

### 📁 目录说明
* `web_attendance.py`: 网页端主程序
* `face_db/encodings.pkl`: 预提取的人脸特征库文件
* `yolo11n-face.pt`: YOLO 人脸检测模型
