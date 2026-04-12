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

## 📸 项目效果展示
### 1. 系统主界面
支持实时开启摄像头。
![网页主界面](https://github.com/user-attachments/assets/b5eeda43-cba3-4328-b92b-895c652bb097)

### 2. 实时识别与侧边栏统计
侧边栏会实时更新当前已签到的人数和名单。
![运行界面](https://github.com/user-attachments/assets/a7d0e659-a473-4000-995c-e7bb3000ba2c)

### 3. 最终识别结果
系统准确识别出人脸，并自动在签到记录中添加姓名、日期和精确时间。
![识别结果展示](https://github.com/user-attachments/assets/8d16a7d0-2860-4ea2-8918-98b8040f1cdb)

